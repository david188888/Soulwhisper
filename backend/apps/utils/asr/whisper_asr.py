import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from pathlib import Path
import os
import logging
from functools import lru_cache

# Configure logging
logger = logging.getLogger(__name__)

# Set GPU or CPU
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Set model path, using absolute path of project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
MODEL_PATH = os.path.join(BASE_DIR, "ASR_model/model")

# Supported audio formats
SUPPORTED_AUDIO_EXTENSIONS = ('.wav', '.mp3', '.m4a', '.flac')

# Model related variables
model = None
processor = None
pipe = None

@lru_cache(maxsize=1)
def load_model():
    """
    Load speech recognition model
    Use lru_cache decorator to ensure model is only loaded once
    """
    global model, processor, pipe
    
    if model is None:
        try:
            logger.info(f"Loading ASR model, device: {device}, precision: {torch_dtype}")
            
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
            
            logger.info("ASR model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
    return True

def validate_audio_file(file_path):
    """
    Validate if audio file is valid
    Args:
        file_path: Audio file path
    Returns:
        (bool, str): (is valid, error message)
    """
    path = Path(file_path)
    
    if not path.exists():
        return False, f"File does not exist: {file_path}"
    
    if path.suffix.lower() not in SUPPORTED_AUDIO_EXTENSIONS:
        return False, f"Unsupported audio format: {path.suffix}, supported formats: {SUPPORTED_AUDIO_EXTENSIONS}"
    
    if path.stat().st_size == 0:
        return False, f"File is empty: {file_path}"
    
    return True, ""

def transcribe_audio(audio_file_path):
    """
    Transcribe a single audio file
    Args:
        audio_file_path: Audio file path
    Returns:
        Transcription text result or error message
    """
    # Validate file
    is_valid, error_msg = validate_audio_file(audio_file_path)
    if not is_valid:
        return {"error": error_msg}
    
    # Ensure model is loaded
    if not load_model():
        return {"error": "Unable to load speech recognition model"}
    
    try:
        # Perform transcription
        logger.info(f"Transcribing file: {audio_file_path}")
        result = pipe(str(audio_file_path))
        logger.info(f"Transcription completed: {audio_file_path}")
        return {"text": result["text"]}
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        return {"error": f"Error during transcription: {str(e)}"}
