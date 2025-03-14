import os
import torch
import numpy as np
import onnxruntime
from pathlib import Path
import logging
from functools import lru_cache

# 配置日志
logger = logging.getLogger(__name__)

# GPU验证函数
def check_gpu_status():
    """验证GPU状态并返回详细信息"""
    gpu_info = {
        "cuda_available": torch.cuda.is_available(),
        "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "无GPU",
        "cuda_version": torch.version.cuda if hasattr(torch.version, 'cuda') else "未知",
    }
    
    # 记录GPU信息
    logger.info(f"CUDA可用: {gpu_info['cuda_available']}")
    logger.info(f"GPU数量: {gpu_info['gpu_count']}")
    logger.info(f"GPU名称: {gpu_info['gpu_name']}")
    logger.info(f"CUDA版本: {gpu_info['cuda_version']}")
    
    # 检查ONNX Runtime的GPU支持
    onnx_providers = onnxruntime.get_available_providers()
    logger.info(f"ONNX可用提供者: {onnx_providers}")
    if 'CUDAExecutionProvider' not in onnx_providers:
        logger.warning("ONNX Runtime不支持CUDA，请安装GPU版本的ONNX Runtime")
    
    return gpu_info

# 设置路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
ONNX_MODEL_PATH = os.path.join(BASE_DIR, "backend/ASR_model/onnx_opt")
TEMP_AUDIO_PATH = os.path.join(BASE_DIR, "backend/temp_audio")
WHISPER_MODEL_PATH = os.path.join(BASE_DIR, "backend/ASR_model/model")

# 设置GPU或CPU
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# 音频分块处理的时长设置 (单位：秒)
CHUNK_LENGTH = 30  # Whisper的典型接收场长度为30秒
CHUNK_OVERLAP = 1  # 块之间的重叠时间，有助于平滑拼接

# 模型相关变量
processor = None
encoder_session = None
decoder_session = None

@lru_cache(maxsize=1)
def load_model():
    """
    加载ONNX语音识别模型
    使用lru_cache装饰器确保模型只被加载一次
    """
    from transformers import AutoProcessor
    global processor, encoder_session, decoder_session
    
    if encoder_session is None or decoder_session is None:
        try:
            # 检查GPU状态
            gpu_info = check_gpu_status()
            logger.info(f"正在加载ONNX ASR模型，设备: {device}")
            
            # 加载处理器
            processor = AutoProcessor.from_pretrained(
                WHISPER_MODEL_PATH,
                local_files_only=True,
            )
            
            # 加载ONNX模型
            encoder_path = os.path.join(ONNX_MODEL_PATH, "encoder_model.onnx")
            decoder_path = os.path.join(ONNX_MODEL_PATH, "decoder_model.onnx")
            
            # 创建ONNX运行时会话，添加GPU优化设置
            providers = []
            provider_options = []
            
            if torch.cuda.is_available() and 'CUDAExecutionProvider' in onnxruntime.get_available_providers():
                # GPU优化设置
                cuda_provider_options = {
                    'device_id': 0,
                    'arena_extend_strategy': 'kNextPowerOfTwo',
                    'gpu_mem_limit': 2 * 1024 * 1024 * 1024,  # 2GB GPU内存限制，根据实际情况调整
                    'cudnn_conv_algo_search': 'EXHAUSTIVE',
                    'do_copy_in_default_stream': True,
                }
                providers.append('CUDAExecutionProvider')
                provider_options.append(cuda_provider_options)
            
            # 始终添加CPU提供者作为备选
            providers.append('CPUExecutionProvider')
            provider_options.append({})
            
            # 创建会话
            encoder_session = onnxruntime.InferenceSession(
                encoder_path, 
                providers=providers,
                provider_options=provider_options
            )
            decoder_session = onnxruntime.InferenceSession(
                decoder_path, 
                providers=providers,
                provider_options=provider_options
            )
            
            # 记录会话信息
            logger.info(f"Encoder会话提供者: {encoder_session.get_providers()}")
            logger.info(f"Decoder会话提供者: {decoder_session.get_providers()}")
            logger.info("ONNX ASR模型加载成功")
            return True
        except Exception as e:
            logger.error(f"加载ONNX模型时出错: {str(e)}")
            return False
    return True

def split_audio(audio, sr, chunk_length=CHUNK_LENGTH, chunk_overlap=CHUNK_OVERLAP):
    """
    将长音频分割成重叠的小块
    
    Args:
        audio: 音频数组
        sr: 采样率
        chunk_length: 每块的长度（秒）
        chunk_overlap: 块之间的重叠时间（秒）
    
    Returns:
        块列表和每块的时间信息
    """
    # 计算每个块的样本数
    chunk_length_samples = int(chunk_length * sr)
    chunk_overlap_samples = int(chunk_overlap * sr)
    stride = chunk_length_samples - chunk_overlap_samples
    
    # 音频总长度
    audio_length_samples = len(audio)
    
    # 如果音频长度小于等于块长度，则直接返回整个音频
    if audio_length_samples <= chunk_length_samples:
        return [audio], [(0, len(audio)/sr)]
    
    # 分割音频块
    chunks = []
    time_info = []
    
    # 计算可以提取的块数
    num_chunks = max(1, int(np.ceil((audio_length_samples - chunk_overlap_samples) / stride)))
    
    for i in range(num_chunks):
        start_sample = i * stride
        end_sample = min(start_sample + chunk_length_samples, audio_length_samples)
        
        # 如果是最后一个块且长度太短，则向前调整起始位置
        if i == num_chunks - 1 and end_sample - start_sample < chunk_length_samples // 2:
            start_sample = max(0, audio_length_samples - chunk_length_samples)
        
        # 提取音频块
        chunk = audio[start_sample:end_sample]
        chunks.append(chunk)
        
        # 记录时间信息
        start_time = start_sample / sr
        end_time = end_sample / sr
        time_info.append((start_time, end_time))
    
    logger.info(f"将{len(audio)/sr:.2f}秒的音频分割成{len(chunks)}个块")
    for i, (start, end) in enumerate(time_info):
        logger.info(f"  块 {i+1}: {start:.2f}s - {end:.2f}s (长度: {end-start:.2f}s)")
    
    return chunks, time_info

def transcribe_chunk(audio_chunk):
    """使用ONNX模型转录单个音频块"""
    if not load_model():
        return None
    
    try:
        # 使用processor进行特征提取
        inputs = processor(audio_chunk, sampling_rate=16000, return_tensors="np")
        input_features = inputs.input_features
        
        # Encoder推理
        encoder_inputs = {encoder_session.get_inputs()[0].name: input_features}
        encoder_outputs = encoder_session.run(None, encoder_inputs)
        encoder_hidden_states = encoder_outputs[0]
        
        # 准备解码器输入
        tokenizer = processor.tokenizer
        decoder_start_tokens = "<|startoftranscript|><|zh|><|transcribe|>"
        decoder_input_ids = tokenizer(decoder_start_tokens, return_tensors="np").input_ids
        
        # 确保decoder_input_ids是int64类型
        decoder_input_ids = decoder_input_ids.astype(np.int64)
        
        # 生成变量
        generated_ids = decoder_input_ids
        max_length = 256
        
        # 解码过程
        while generated_ids.shape[1] < max_length:
            decoder_inputs = {
                decoder_session.get_inputs()[0].name: generated_ids,
                decoder_session.get_inputs()[1].name: encoder_hidden_states
            }
            
            decoder_outputs = decoder_session.run(None, decoder_inputs)
            logits = decoder_outputs[0]
            
            next_token_logits = logits[:, -1, :]
            next_token_id = np.argmax(next_token_logits, axis=-1)
            
            # 确保next_token_id是int64类型
            next_token_id = np.expand_dims(next_token_id, axis=-1).astype(np.int64)
            generated_ids = np.concatenate([generated_ids, next_token_id], axis=-1)
            
            if next_token_id[0, 0] == tokenizer.eos_token_id:
                break
        
        # 将token ID转换为文本
        transcription = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        return transcription
    except Exception as e:
        logger.error(f"转录音频块时出错: {str(e)}")
        return None

def process_transcriptions(transcriptions, time_info):
    """处理并拼接转录结果"""
    if len(transcriptions) == 1:
        return transcriptions[0]
    
    # 将所有转录结果合并，考虑重叠部分
    final_text = ""
    for i, (trans, (start_time, end_time)) in enumerate(zip(transcriptions, time_info)):
        # 第一个块直接添加
        if i == 0:
            final_text += trans
        else:
            # 追加新内容
            final_text += " " + trans
    
    return final_text.strip()

def transcribe_audio_with_onnx(audio_path):
    """
    使用ONNX模型转录单个音频文件
    Args:
        audio_path: 音频文件路径
    Returns:
        转录文本结果或错误信息
    """
    import librosa
    
    # 确保模型已加载
    if not load_model():
        return {"error": "无法加载ONNX语音识别模型"}
    
    try:
        # 加载音频
        logger.info(f"正在加载音频: {audio_path}")
        audio, sr = librosa.load(audio_path, sr=16000)
        
        # 确保音频是单声道
        if len(audio.shape) > 1:
            audio = audio.mean(axis=0)
        
        # 检查音频长度
        audio_length_seconds = len(audio) / sr
        logger.info(f"音频长度: {audio_length_seconds:.2f}秒")
        
        # 如果音频长度超过Whisper的接收场长度，则分块处理
        if audio_length_seconds > CHUNK_LENGTH:
            logger.info(f"音频长度超过{CHUNK_LENGTH}秒，将使用分块处理")
            
            # 分割音频为块
            chunks, time_info = split_audio(audio, sr)
            
            # 处理每个块
            transcriptions = []
            for i, chunk in enumerate(chunks):
                logger.info(f"处理块 {i+1}/{len(chunks)}")
                trans = transcribe_chunk(chunk)
                if trans:
                    transcriptions.append(trans)
                    logger.info(f"块 {i+1} 转录完成")
                else:
                    logger.warning(f"块 {i+1} 转录失败")
            
            # 合并转录结果
            if transcriptions:
                final_text = process_transcriptions(transcriptions, time_info)
                logger.info(f"所有块处理完成，合并结果")
                return {"text": final_text}
            else:
                return {"error": "所有块转录失败"}
        else:
            # 短音频直接处理
            logger.info("音频长度适中，直接处理")
            transcription = transcribe_chunk(audio)
            if transcription:
                return {"text": transcription}
            else:
                return {"error": "转录失败"}
    except Exception as e:
        logger.error(f"ONNX转录过程中出错: {str(e)}")
        return {"error": f"ONNX转录过程中出错: {str(e)}"} 