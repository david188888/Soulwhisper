"""
语音识别工具

提供基于Transformer的语音转文字功能
"""

# 导出主要功能函数
from .whisper_asr import transcribe_audio, load_model 