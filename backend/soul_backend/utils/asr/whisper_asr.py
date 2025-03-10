import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from pathlib import Path
import os
import logging
from functools import lru_cache

# 配置日志
logger = logging.getLogger(__name__)

# 设置GPU或CPU
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# 设置模型路径，使用项目根目录的绝对路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
MODEL_PATH = os.path.join(BASE_DIR, "ASR_model/model")

# 支持的音频格式
SUPPORTED_AUDIO_EXTENSIONS = ('.wav', '.mp3', '.m4a', '.flac')

# 模型相关变量
model = None
processor = None
pipe = None

@lru_cache(maxsize=1)
def load_model():
    """
    加载语音识别模型
    使用lru_cache装饰器确保模型只被加载一次
    """
    global model, processor, pipe
    
    if model is None:
        try:
            logger.info(f"正在加载ASR模型，设备: {device}, 精度: {torch_dtype}")
            
            model = AutoModelForSpeechSeq2Seq.from_pretrained(
                MODEL_PATH,
                torch_dtype=torch_dtype,
                local_files_only=True,
            ).to(device)
            
            processor = AutoProcessor.from_pretrained(
                MODEL_PATH,
                local_files_only=True,
            )
            
            pipe = pipeline(
                "automatic-speech-recognition",
                model=model,
                tokenizer=processor.tokenizer,
                feature_extractor=processor.feature_extractor,
                torch_dtype=torch_dtype,
                device=device,
            )
            
            logger.info("ASR模型加载成功")
            return True
        except Exception as e:
            logger.error(f"加载模型时出错: {str(e)}")
            return False
    return True

def validate_audio_file(file_path):
    """
    验证音频文件是否有效
    Args:
        file_path: 音频文件路径
    Returns:
        (bool, str): (是否有效, 错误信息)
    """
    path = Path(file_path)
    
    if not path.exists():
        return False, f"文件不存在: {file_path}"
    
    if path.suffix.lower() not in SUPPORTED_AUDIO_EXTENSIONS:
        return False, f"不支持的音频格式: {path.suffix}，支持的格式: {SUPPORTED_AUDIO_EXTENSIONS}"
    
    if path.stat().st_size == 0:
        return False, f"文件为空: {file_path}"
    
    return True, ""

def transcribe_audio(audio_file_path):
    """
    转录单个音频文件
    Args:
        audio_file_path: 音频文件路径
    Returns:
        转录文本结果或错误信息
    """
    # 验证文件
    is_valid, error_msg = validate_audio_file(audio_file_path)
    if not is_valid:
        return {"error": error_msg}
    
    # 确保模型已加载
    if not load_model():
        return {"error": "无法加载语音识别模型"}
    
    try:
        # 进行转录
        logger.info(f"正在转录文件: {audio_file_path}")
        result = pipe(str(audio_file_path))
        logger.info(f"转录完成: {audio_file_path}")
        return {"text": result["text"]}
    except Exception as e:
        logger.error(f"转录过程中出错: {str(e)}")
        return {"error": f"转录过程中出错: {str(e)}"}
