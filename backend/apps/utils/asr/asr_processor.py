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
from pathlib import Path
from dashscope import MultiModalConversation
import concurrent.futures
# from backend.config.settings import *  # Assume all settings need to be imported

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


# def reduce_noise(audio_path):
#     """
#     Perform noise reduction on audio file
#     Dynamically adjust window size to adapt to different audio lengths
#     """
#     try:
#         data, rate = sf.read(audio_path)
#         if data.dtype != np.float32:
#             data = data.astype(np.float32)
#         
#         # Calculate appropriate window size
#         # Ensure window size is not larger than audio length and is a power of 2
#         audio_length = len(data)
#         window_size = min(1024, audio_length)  # Default window size is 1024
#         # Find the closest power of 2 to audio length
#         while window_size > audio_length:
#             window_size //= 2
#         if window_size < 2:  # Ensure window size is at least 2
#             window_size = 2
#             
#         reduced_noise = nr.reduce_noise(
#             y=data,
#             sr=rate,
#             prop_decrease=0.95,
#             win_length=window_size,  # Use dynamically calculated window size
#             n_fft=window_size,  # FFT window size also adjusted accordingly
#             n_std_thresh_stationary=1.5,
#             stationary=True,
#         )
#         
#         output_path = str(Path(audio_path).parent / f"denoised_{Path(audio_path).name}")
#         sf.write(output_path, reduced_noise, rate)
#         return output_path
#     except Exception as e:
#         logger.error(f"Noise reduction processing failed: {str(e)}")
#         return audio_path


def detect_emotion(audio_file_path):
    """
    Use Tongyi's speech large model API for emotion recognition
    Return format: {'emotion_type': 'happy/sad/angry', 'emotion_intensity': 1-10}
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
            # Extract text content from response
            content_text = ""
            for content in response.get('output', {}).get('choices', [{}])[0].get('message', {}).get('content', []):
                if 'text' in content:
                    content_text += content['text']
            
            # Try to parse JSON or extract emotion information from text
            try:
                import json
                import re
                
                # Try direct JSON parsing
                try:
                    result = json.loads(content_text)
                    if 'emotion_type' in result and 'emotion_intensity' in result:
                        # Ensure emotion type is one we support
                        if result['emotion_type'] not in ['happy', 'sad', 'angry']:
                            result['emotion_type'] = 'neutral'
                        # Ensure emotion intensity is in range 1-10
                        intensity = int(result['emotion_intensity'])
                        result['emotion_intensity'] = max(1, min(10, intensity))
                        return result
                except:
                    pass
                
                # If JSON parsing fails, try to extract from text
                emotion_match = re.search(r'(happy|sad|angry)', content_text.lower())
                emotion_type = emotion_match.group(1) if emotion_match else 'neutral'
                
                intensity_match = re.search(r'intensity.*?(\d+)', content_text.lower())
                if not intensity_match:
                    intensity_match = re.search(r'(\d+)/10', content_text.lower())
                emotion_intensity = int(intensity_match.group(1)) if intensity_match else 5
                
                # Ensure emotion intensity is in range 1-10
                emotion_intensity = max(1, min(10, emotion_intensity))
                
                return {
                    'emotion_type': emotion_type,
                    'emotion_intensity': emotion_intensity
                }
            except Exception as e:
                logger.error(f"Failed to parse emotion analysis result: {str(e)}")
                return {
                    'emotion_type': 'neutral',
                    'emotion_intensity': 5
                }
        else:
            logger.error(f"Emotion recognition API call failed: {response.get('message', 'Unknown error')}")
            return {'emotion_type': 'neutral', 'emotion_intensity': 5}
    except Exception as e:
        logger.error(f"Error in emotion recognition process: {str(e)}")
        return {'emotion_type': 'neutral', 'emotion_intensity': 5}


def transcribe_audio(audio_file_path):
    """
    Use Xunfei long speech recognition service to transcribe audio file
    Return format: {'text': 'recognized text content'}
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
            raise Exception(f"Xunfei ASR error: {result.get('descInfo', 'Unknown error')}")
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
        logger.error(f"Error in speech recognition process: {str(e)}")
        return {'error': str(e)}
    # 不再需要删除降噪文件的cleanup代码
    # finally:
    #     if audio_file_path and audio_file_path != audio_file_path:
    #         try:
    #             os.remove(audio_file_path)
    #         except Exception as e:
    #             logger.error(f"Failed to clean up denoised audio file: {str(e)}")

def process_audio(audio_file_path):
    """
    Process audio file in parallel: perform speech transcription and emotion recognition simultaneously
    Return format: {'text': 'text content', 'emotion_type': 'emotion type', 'emotion_intensity': emotion intensity}
    """
    try:
        # 直接使用原始音频文件，不进行降噪处理
        # denoised_path = reduce_noise(audio_file_path)
        
        # Use ThreadPoolExecutor to perform speech transcription and emotion recognition in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit two tasks - 直接使用原始音频文件
            transcribe_future = executor.submit(transcribe_audio, audio_file_path)
            emotion_future = executor.submit(detect_emotion, audio_file_path)
            
            # Get results
            transcribe_result = transcribe_future.result()
            emotion_result = emotion_future.result()
            
        # Merge results
        result = {}
        
        # Add speech transcription result
        if 'error' in transcribe_result:
            result['error'] = transcribe_result['error']
            return result
        else:
            result['text'] = transcribe_result['text']
        
        # Add emotion analysis result
        result['emotion_type'] = emotion_result.get('emotion_type', 'neutral')
        result['emotion_intensity'] = emotion_result.get('emotion_intensity', 5)
        
        return result
    except Exception as e:
        logger.error(f"Error processing audio file: {str(e)}")
        return {'error': str(e)}
    # 不再需要清理降噪文件
    # finally:
    #     if denoised_path and denoised_path != audio_file_path:
    #         try:
    #             os.remove(denoised_path)
    #         except Exception as e:
    #             logger.error(f"Failed to clean up denoised audio file: {str(e)}")