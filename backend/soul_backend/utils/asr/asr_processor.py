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
    """
    try:
        data, rate = sf.read(audio_path)
        if data.dtype != np.float32:
            data = data.astype(np.float32)
        reduced_noise = nr.reduce_noise(
            y=data,
            sr=rate,
            prop_decrease=0.95,
            win_length= 1024,
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
    """
    messages = [
        {
            "role": "system", 
            "content": [{"text": "You are a helpful assistant, and good at judging user emotions"}]},
        {
            "role": "user",
            "content": [{"audio": audio_file_path}, {"text": "What emotions does this audio clip express? You only need to judge the three emotions [happy, angry, sad] and only output the emotion label."}],
        }
    ]

    response = MultiModalConversation.call(model="qwen-audio-turbo-latest", messages=messages,api_key=settings.AUDIO_TURBO_API_KEY)
    if response['status_code'] == 200:
        # 假设返回的情感信息在 response 中
        emotion_info = response.get('output', {}).get('choices', [{}])[0].get('message', {}).get('content', [{}])
        return emotion_info
    else:
        return {'error': '情感识别失败'}


def transcribe_audio(audio_file_path):
    """
    使用讯飞长语音识别服务转写音频文件
    """
    denoised_path = None
    try:
        denoised_path = reduce_noise(audio_file_path)
        api = RequestApi(
            appid=settings.XUNFEI_APPID,
            secret_key=settings.XUNFEI_API_SECRET,
            upload_file_path=denoised_path
        )
        result = api.get_result()
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
        # 调用情感识别函数
        emotion_info = detect_emotion(denoised_path)
        return {'text': final_text, 'emotion': emotion_info}
    except Exception as e:
        logger.error(f"语音识别过程出错: {str(e)}")
        return {'error': str(e)}
    finally:
        if denoised_path and denoised_path != audio_file_path:
            try:
                os.remove(denoised_path)
            except Exception as e:
                logger.error(f"清理降噪音频文件失败: {str(e)}") 