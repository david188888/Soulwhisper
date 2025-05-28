import os
import torch
import numpy as np
import onnxruntime
from pathlib import Path
import logging
from functools import lru_cache

# Configure logging
logger = logging.getLogger(__name__)

# GPU validation function
def check_gpu_status():
    """Validate GPU status and return detailed information"""
    gpu_info = {
        "cuda_available": torch.cuda.is_available(),
        "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU",
        "cuda_version": torch.version.cuda if hasattr(torch.version, 'cuda') else "Unknown",
    }
    
    # Log GPU information
    logger.info(f"CUDA available: {gpu_info['cuda_available']}")
    logger.info(f"GPU count: {gpu_info['gpu_count']}")
    logger.info(f"GPU name: {gpu_info['gpu_name']}")
    logger.info(f"CUDA version: {gpu_info['cuda_version']}")
    
    # Check ONNX Runtime GPU support
    onnx_providers = onnxruntime.get_available_providers()
    logger.info(f"ONNX available providers: {onnx_providers}")
    if 'CUDAExecutionProvider' not in onnx_providers:
        logger.warning("ONNX Runtime does not support CUDA, please install GPU version of ONNX Runtime")
    
    return gpu_info

# Set paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
ONNX_MODEL_PATH = os.path.join(BASE_DIR, "backend/ASR_model/onnx_opt")
TEMP_AUDIO_PATH = os.path.join(BASE_DIR, "backend/temp_audio")
WHISPER_MODEL_PATH = os.path.join(BASE_DIR, "backend/ASR_model/model")

# Set GPU or CPU
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Audio chunk processing duration settings (in seconds)
CHUNK_LENGTH = 30  # Whisper's typical receptive field length is 30 seconds
CHUNK_OVERLAP = 1  # Overlap time between chunks, helps with smooth concatenation

# Model related variables
processor = None
encoder_session = None
decoder_session = None

@lru_cache(maxsize=1)
def load_model():
    """
    Load ONNX speech recognition model
    Use lru_cache decorator to ensure model is only loaded once
    """
    from transformers import AutoProcessor
    global processor, encoder_session, decoder_session
    
    if encoder_session is None or decoder_session is None:
        try:
            # Check GPU status
            gpu_info = check_gpu_status()
            logger.info(f"Loading ONNX ASR model, device: {device}")
            
            # Load processor
            processor = AutoProcessor.from_pretrained(
                WHISPER_MODEL_PATH,
                local_files_only=True,
            )
            
            # Load ONNX models
            encoder_path = os.path.join(ONNX_MODEL_PATH, "encoder_model.onnx")
            decoder_path = os.path.join(ONNX_MODEL_PATH, "decoder_model.onnx")
            
            # Create ONNX runtime sessions, add GPU optimization settings
            providers = []
            provider_options = []
            
            if torch.cuda.is_available() and 'CUDAExecutionProvider' in onnxruntime.get_available_providers():
                # GPU optimization settings
                cuda_provider_options = {
                    'device_id': 0,
                    'arena_extend_strategy': 'kNextPowerOfTwo',
                    'gpu_mem_limit': 2 * 1024 * 1024 * 1024,  # 2GB GPU memory limit, adjust based on actual situation
                    'cudnn_conv_algo_search': 'EXHAUSTIVE',
                    'do_copy_in_default_stream': True,
                }
                providers.append('CUDAExecutionProvider')
                provider_options.append(cuda_provider_options)
            
            # Always add CPU provider as fallback
            providers.append('CPUExecutionProvider')
            provider_options.append({})
            
            # Create sessions
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
            
            # Log session information
            logger.info(f"Encoder session provider: {encoder_session.get_providers()}")
            logger.info(f"Decoder session provider: {decoder_session.get_providers()}")
            logger.info("ONNX ASR model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading ONNX model: {str(e)}")
            return False
    return True

def split_audio(audio, sr, chunk_length=CHUNK_LENGTH, chunk_overlap=CHUNK_OVERLAP):
    """
    Split long audio into overlapping chunks
    
    Args:
        audio: Audio array
        sr: Sampling rate
        chunk_length: Length of each chunk (seconds)
        chunk_overlap: Overlap time between chunks (seconds)
    
    Returns:
        List of chunks and time information for each chunk
    """
    # Calculate samples per chunk
    chunk_length_samples = int(chunk_length * sr)
    chunk_overlap_samples = int(chunk_overlap * sr)
    stride = chunk_length_samples - chunk_overlap_samples
    
    # Total audio length
    audio_length_samples = len(audio)
    
    # If audio length is less than or equal to chunk length, return the entire audio
    if audio_length_samples <= chunk_length_samples:
        return [audio], [(0, len(audio)/sr)]
    
    # Split audio chunks
    chunks = []
    time_info = []
    
    # Calculate number of chunks that can be extracted
    num_chunks = max(1, int(np.ceil((audio_length_samples - chunk_overlap_samples) / stride)))
    
    for i in range(num_chunks):
        start_sample = i * stride
        end_sample = min(start_sample + chunk_length_samples, audio_length_samples)
        
        # If it's the last chunk and too short, adjust start position forward
        if i == num_chunks - 1 and end_sample - start_sample < chunk_length_samples // 2:
            start_sample = max(0, audio_length_samples - chunk_length_samples)
        
        # Extract audio chunk
        chunk = audio[start_sample:end_sample]
        chunks.append(chunk)
        
        # Record time information
        start_time = start_sample / sr
        end_time = end_sample / sr
        time_info.append((start_time, end_time))
    
    logger.info(f"Split {len(audio)/sr:.2f} seconds of audio into {len(chunks)} chunks")
    for i, (start, end) in enumerate(time_info):
        logger.info(f"  Chunk {i+1}: {start:.2f}s - {end:.2f}s (length: {end-start:.2f}s)")
    
    return chunks, time_info

def transcribe_chunk(audio_chunk):
    """Transcribe a single audio chunk using ONNX model"""
    if not load_model():
        return None
    
    try:
        # Use processor for feature extraction
        inputs = processor(audio_chunk, sampling_rate=16000, return_tensors="np")
        input_features = inputs.input_features
        
        # Encoder inference
        encoder_inputs = {encoder_session.get_inputs()[0].name: input_features}
        encoder_outputs = encoder_session.run(None, encoder_inputs)
        encoder_hidden_states = encoder_outputs[0]
        
        # Prepare decoder input
        tokenizer = processor.tokenizer
        decoder_start_tokens = "<|startoftranscript|><|zh|><|transcribe|>"
        decoder_input_ids = tokenizer(decoder_start_tokens, return_tensors="np").input_ids
        
        # Ensure decoder_input_ids is int64 type
        decoder_input_ids = decoder_input_ids.astype(np.int64)
        
        # Generation variables
        generated_ids = decoder_input_ids
        max_length = 256
        
        # Decoding process
        while generated_ids.shape[1] < max_length:
            decoder_inputs = {
                decoder_session.get_inputs()[0].name: generated_ids,
                decoder_session.get_inputs()[1].name: encoder_hidden_states
            }
            
            decoder_outputs = decoder_session.run(None, decoder_inputs)
            logits = decoder_outputs[0]
            
            next_token_logits = logits[:, -1, :]
            next_token_id = np.argmax(next_token_logits, axis=-1)
            
            # Ensure next_token_id is int64 type
            next_token_id = np.expand_dims(next_token_id, axis=-1).astype(np.int64)
            generated_ids = np.concatenate([generated_ids, next_token_id], axis=-1)
            
            if next_token_id[0, 0] == tokenizer.eos_token_id:
                break
        
        # Convert token IDs to text
        transcription = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        return transcription
    except Exception as e:
        logger.error(f"Error transcribing audio chunk: {str(e)}")
        return None

def process_transcriptions(transcriptions, time_info):
    """Process and concatenate transcription results"""
    if len(transcriptions) == 1:
        return transcriptions[0]
    
    # Merge all transcription results, considering overlapping parts
    final_text = ""
    for i, (trans, (start_time, end_time)) in enumerate(zip(transcriptions, time_info)):
        # Add first chunk directly
        if i == 0:
            final_text += trans
        else:
            # Append new content
            final_text += " " + trans
    
    return final_text.strip()

def transcribe_audio_with_onnx(audio_path):
    """
    Transcribe a single audio file using ONNX model
    Args:
        audio_path: Audio file path
    Returns:
        Transcription text result or error information
    """
    import librosa
    
    # Ensure model is loaded
    if not load_model():
        return {"error": "Unable to load ONNX speech recognition model"}
    
    try:
        # Load audio
        logger.info(f"Loading audio: {audio_path}")
        audio, sr = librosa.load(audio_path, sr=16000)
        
        # Ensure audio is mono
        if len(audio.shape) > 1:
            audio = audio.mean(axis=0)
        
        # Check audio length
        audio_length_seconds = len(audio) / sr
        logger.info(f"Audio length: {audio_length_seconds:.2f} seconds")
        
        # If audio length exceeds Whisper's receptive field length, process in chunks
        if audio_length_seconds > CHUNK_LENGTH:
            logger.info(f"Audio length exceeds {CHUNK_LENGTH} seconds, using chunk processing")
            
            # Split audio into chunks
            chunks, time_info = split_audio(audio, sr)
            
            # Process each chunk
            transcriptions = []
            for i, chunk in enumerate(chunks):
                logger.info(f"Processing chunk {i+1}/{len(chunks)}")
                trans = transcribe_chunk(chunk)
                if trans:
                    transcriptions.append(trans)
                    logger.info(f"Chunk {i+1} transcription completed")
                else:
                    logger.warning(f"Chunk {i+1} transcription failed")
            
            # Merge transcription results
            if transcriptions:
                final_text = process_transcriptions(transcriptions, time_info)
                logger.info(f"All chunks processed, merged results")
                return {"text": final_text}
            else:
                return {"error": "All chunks transcription failed"}
        else:
            # Short audio directly processed
            logger.info("Audio length suitable, directly processed")
            transcription = transcribe_chunk(audio)
            if transcription:
                return {"text": transcription}
            else:
                return {"error": "Transcription failed"}
    except Exception as e:
        logger.error(f"Error in ONNX transcription: {str(e)}")
        return {"error": f"Error in ONNX transcription: {str(e)}"} 