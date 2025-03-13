from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
from pathlib import Path
import uuid
import logging
# 更新导入以使用新的 ASR 处理脚本
from ..utils.asr.asr_processor import transcribe_audio, detect_emotion

logger = logging.getLogger(__name__)

@csrf_exempt
def asr_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST请求'}, status=405)
    
    if 'audio_file' not in request.FILES:
        return JsonResponse({'error': '没有上传音频文件'}, status=400)
    
    audio_file = request.FILES['audio_file']
    file_extension = os.path.splitext(audio_file.name)[1].lower()
    if file_extension not in ['.wav', '.mp3', '.m4a', '.flac']:
        return JsonResponse({'error': f'不支持的音频格式: {file_extension}'}, status=400)
    
    TEMP_DIR = Path(settings.BASE_DIR) / 'temp_audio'
    TEMP_DIR.mkdir(exist_ok=True)
    temp_file = TEMP_DIR / f"{uuid.uuid4()}{file_extension}"
    
    try:
        with open(temp_file, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        
        # 始终使用讯飞ASR接口进行转写
        transcription_result = transcribe_audio(str(temp_file))
        if 'error' in transcription_result:
            raise Exception(transcription_result['error'])
        
        return JsonResponse({"text": transcription_result['text']})
    except Exception as e:
        logger.error(f"处理语音转写时出错: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        if temp_file.exists():
            os.remove(temp_file)

@csrf_exempt
def emotion_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST请求'}, status=405)
    
    if 'audio_file' not in request.FILES:
        return JsonResponse({'error': '没有上传音频文件'}, status=400)
    
    audio_file = request.FILES['audio_file']
    file_extension = os.path.splitext(audio_file.name)[1].lower()
    if file_extension not in ['.wav', '.mp3', '.m4a', '.flac']:
        return JsonResponse({'error': f'不支持的音频格式: {file_extension}'}, status=400)
    
    TEMP_DIR = Path(settings.BASE_DIR) / 'temp_audio'
    TEMP_DIR.mkdir(exist_ok=True)
    temp_file = TEMP_DIR / f"{uuid.uuid4()}{file_extension}"
    
    try:
        with open(temp_file, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        
        # 调用情感识别函数
        emotion_info = detect_emotion(str(temp_file))
        if 'error' in emotion_info:
            raise Exception(emotion_info['error'])
        
        return JsonResponse({"emotion": emotion_info})
    except Exception as e:
        logger.error(f"处理情感识别时出错: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        if temp_file.exists():
            os.remove(temp_file)
