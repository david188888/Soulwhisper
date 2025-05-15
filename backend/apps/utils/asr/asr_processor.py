# -*- coding: utf-8 -*-
import logging
import base64
import hashlib
import hmac
import json
import os
import time
from django.conf import settings
import requests
import urllib
import soundfile as sf
import noisereduce as nr
import numpy as np
from pathlib import Path
from dashscope import MultiModalConversation
import concurrent.futures
# from backend.config.settings import *  # 假设需要导入所有设置






lfasr_host = 'https://raasr.xfyun.cn/v2/api'
api_upload = '/upload'
api_get_result = '/getResult'

logger = logging.getLogger(__name__)

class RequestApi(object):
    def __init__(self, appid, secret_key, upload_file_path):
        self.appid = appid
        self.secret_key = secret_key
        self.upload_file_path = upload_file_path
        self.ts = str(int(time.time()))
        self.signa = self.get_signa()

    def get_signa(self):
        appid = self.appid
        secret_key = self.secret_key
        m2 = hashlib.md5()
        m2.update((appid + self.ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        return signa

    def upload(self):
        upload_file_path = self.upload_file_path
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)

        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict["fileSize"] = file_len
        param_dict["fileName"] = file_name
        param_dict["duration"] = "200"
        param_dict['language'] = "en"
        data = open(upload_file_path, 'rb').read(file_len)

        response = requests.post(url =lfasr_host + api_upload+"?"+urllib.parse.urlencode(param_dict),
                                headers = {"Content-type":"application/json"},data=data)
        result = json.loads(response.text)
        return result

    def get_result(self):
        uploadresp = self.upload()
        orderId = uploadresp['content']['orderId']
        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict['orderId'] = orderId
        param_dict['resultType'] = "transfer,predict"
        status = 3
        while status == 3:
            response = requests.post(url=lfasr_host + api_get_result + "?" + urllib.parse.urlencode(param_dict),
                                     headers={"Content-type": "application/json"})
            result = json.loads(response.text)
            status = result['content']['orderInfo']['status']
            if status == 4:
                break
            time.sleep(5)
        return result


def reduce_noise(audio_path):
    """
    对音频文件进行降噪处理
    动态调整窗口大小以适应不同长度的音频
    """
    try:
        data, rate = sf.read(audio_path)
        if data.dtype != np.float32:
            data = data.astype(np.float32)
        
        # 计算适当的窗口大小
        # 确保窗口大小不大于音频长度，并且是2的幂次方
        audio_length = len(data)
        window_size = min(1024, audio_length)  # 默认窗口大小为1024
        # 找到最接近音频长度的2的幂次方
        while window_size > audio_length:
            window_size //= 2
        if window_size < 2:  # 确保窗口大小至少为2
            window_size = 2
            
        reduced_noise = nr.reduce_noise(
            y=data,
            sr=rate,
            prop_decrease=0.95,
            win_length=window_size,  # 使用动态计算的窗口大小
            n_fft=window_size,  # FFT窗口大小也相应调整
            n_std_thresh_stationary=1.5,
            stationary=True,
        )
        
        output_path = str(Path(audio_path).parent / f"denoised_{Path(audio_path).name}")
        sf.write(output_path, reduced_noise, rate)
        return output_path
    except Exception as e:
        logger.error(f"音频降噪处理失败: {str(e)}")
        return audio_path


def detect_emotion(audio_file_path):
    """
    使用通义的语音大模型 API 进行情感识别
    返回格式: {'emotion_type': 'happy/sad/angry', 'emotion_intensity': 1-10}
    """
    messages = [
        {
            "role": "system", 
            "content": [{"text": "You are an emotion analysis assistant. Analyze the emotion in the audio and return only emotion type (happy/sad/angry) and intensity (1-10)."}]},
        {
            "role": "user",
            "content": [
                {"audio": audio_file_path}, 
                {"text": "What emotion is expressed in this audio? Choose only one from (happy, sad, angry) and rate intensity from 1-10. Output JSON format with keys 'emotion_type' and 'emotion_intensity'."}
            ],
        }
    ]

    try:
        response = MultiModalConversation.call(
            model="qwen-audio-turbo-latest", 
            messages=messages,
            api_key=settings.AUDIO_TURBO_API_KEY
        )
        
        if response['status_code'] == 200:
            # 从响应中提取文本内容
            content_text = ""
            for content in response.get('output', {}).get('choices', [{}])[0].get('message', {}).get('content', []):
                if 'text' in content:
                    content_text += content['text']
            
            # 尝试解析JSON或者从文本中提取情感信息
            try:
                import json
                import re
                
                # 尝试直接解析JSON
                try:
                    result = json.loads(content_text)
                    if 'emotion_type' in result and 'emotion_intensity' in result:
                        # 确保情感类型是我们支持的类型
                        if result['emotion_type'] not in ['happy', 'sad', 'angry']:
                            result['emotion_type'] = 'neutral'
                        # 确保情感强度在 1-10 范围内
                        intensity = int(result['emotion_intensity'])
                        result['emotion_intensity'] = max(1, min(10, intensity))
                        return result
                except:
                    pass
                
                # 如果JSON解析失败，尝试从文本中提取
                emotion_match = re.search(r'(happy|sad|angry)', content_text.lower())
                emotion_type = emotion_match.group(1) if emotion_match else 'neutral'
                
                intensity_match = re.search(r'intensity.*?(\d+)', content_text.lower())
                if not intensity_match:
                    intensity_match = re.search(r'(\d+)/10', content_text.lower())
                emotion_intensity = int(intensity_match.group(1)) if intensity_match else 5
                
                # 确保情感强度在 1-10 范围内
                emotion_intensity = max(1, min(10, emotion_intensity))
                
                return {
                    'emotion_type': emotion_type,
                    'emotion_intensity': emotion_intensity
                }
            except Exception as e:
                logger.error(f"解析情感分析结果失败: {str(e)}")
                return {
                    'emotion_type': 'neutral',
                    'emotion_intensity': 5
                }
        else:
            logger.error(f"情感识别API调用失败: {response.get('message', '未知错误')}")
            return {'emotion_type': 'neutral', 'emotion_intensity': 5}
    except Exception as e:
        logger.error(f"情感识别过程出错: {str(e)}")
        return {'emotion_type': 'neutral', 'emotion_intensity': 5}


def transcribe_audio(audio_file_path):
    """
    使用讯飞长语音识别服务转写音频文件
    返回格式: {'text': '识别的文本内容'}
    """
    try:
        # print(f"audio_path is {audio_file_path}")
        api = RequestApi(
            appid=settings.XUNFEI_APPID,
            secret_key=settings.XUNFEI_API_SECRET,
            upload_file_path=audio_file_path
        )
        # print(1111111)
        result = api.get_result()
        # print(f"result is {result}")
        if result.get('code') != '000000':
            raise Exception(f"讯飞ASR错误: {result.get('descInfo', '未知错误')}")
        order_result = json.loads(result['content']['orderResult'])
        final_text = ''
        if 'lattice' in order_result:
            for item in order_result['lattice']:
                json_1best = json.loads(item['json_1best'])
                if 'st' in json_1best:
                    words = json_1best['st'].get('rt', [{}])[0].get('ws', [])
                    text = ''.join(word['cw'][0]['w'] for word in words if word.get('cw'))
                    final_text += text.strip()
        return {'text': final_text}
    except Exception as e:
        logger.error(f"语音识别过程出错: {str(e)}")
        return {'error': str(e)}
    finally:
        if audio_file_path and audio_file_path != audio_file_path:
            try:
                os.remove(audio_file_path)
            except Exception as e:
                logger.error(f"清理降噪音频文件失败: {str(e)}")

def process_audio(audio_file_path):
    """
    并行处理音频文件：同时进行语音转录和情感识别
    返回格式: {'text': '文本内容', 'emotion_type': '情感类型', 'emotion_intensity': 情感强度}
    """
    denoised_path = None
    try:
        # 首先进行降噪处理（只需处理一次）
        denoised_path = reduce_noise(audio_file_path)
        
        # 使用ThreadPoolExecutor并行执行转录和情感识别
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 提交两个任务
            transcribe_future = executor.submit(transcribe_audio, denoised_path)
            emotion_future = executor.submit(detect_emotion, denoised_path)
            
            # 获取结果
            transcribe_result = transcribe_future.result()
            emotion_result = emotion_future.result()
            
        # 合并结果
        result = {}
        
        # 添加文本转录结果
        if 'error' in transcribe_result:
            result['error'] = transcribe_result['error']
            return result
        else:
            result['text'] = transcribe_result['text']
        
        # 添加情感分析结果
        result['emotion_type'] = emotion_result.get('emotion_type', 'neutral')
        result['emotion_intensity'] = emotion_result.get('emotion_intensity', 5)
        
        return result
    except Exception as e:
        logger.error(f"处理音频文件出错: {str(e)}")
        return {'error': str(e)}
    finally:
        if denoised_path and denoised_path != audio_file_path:
            try:
                os.remove(denoised_path)
            except Exception as e:
                logger.error(f"清理降噪音频文件失败: {str(e)}")