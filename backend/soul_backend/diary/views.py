from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import os
from pathlib import Path
import uuid
import logging
from ..utils import analyze_emotion, transcribe_audio
from .models import Diary

logger = logging.getLogger(__name__)

@csrf_exempt
def voice_diary_view(request):
    """
    处理语音日记：上传音频 -> 转文字 -> 情感分析 -> 创建日记
    
    请求方法: POST
    表单数据:
        - audio_file: 语音文件（支持 .wav, .mp3, .m4a, .flac 格式）
        
    响应:
        - 成功: {
            "id": "日记ID",
            "title": "日记标题",
            "content": "转录的文本内容",
            "emotion": "检测到的情感",
            "created_at": "创建时间"
        }
        - 失败: {"error": "错误信息"}
    """
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST请求'}, status=405)
    
    if 'audio_file' not in request.FILES:
        return JsonResponse({'error': '没有上传音频文件'}, status=400)
    
    audio_file = request.FILES['audio_file']
    
    # 检查文件格式
    file_extension = os.path.splitext(audio_file.name)[1].lower()
    if file_extension not in ['.wav', '.mp3', '.m4a', '.flac']:
        return JsonResponse({'error': f'不支持的音频格式: {file_extension}'}, status=400)
    
    # 创建临时目录
    TEMP_DIR = Path(settings.BASE_DIR) / 'temp_audio'
    TEMP_DIR.mkdir(exist_ok=True)
    
    # 生成临时文件路径
    temp_file = TEMP_DIR / f"{uuid.uuid4()}{file_extension}"
    
    try:
        # 保存音频文件
        with open(temp_file, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        
        # 转录音频
        transcription_result = transcribe_audio(str(temp_file))
        if 'error' in transcription_result:
            raise Exception(transcription_result['error'])
        
        content = transcription_result['text']
        
        # 情感分析
        emotion_result = analyze_emotion(content)
        if 'error' in emotion_result:
            raise Exception(emotion_result['error'])
        
        # 创建日记
        diary = Diary.objects.create(
            user=request.user,
            content=content,
            dominant_emotion=emotion_result['emotion']
        )
        
        response_data = {
            'id': diary.id,
            'content': diary.content,
            'emotion': diary.dominant_emotion,
            'created_at': diary.created_at.isoformat()
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"处理语音日记时出错: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
        
    finally:
        # 清理临时文件
        if temp_file.exists():
            os.remove(temp_file)
