# SoulWhisper POC Demo - Configuration File

# Basic Information
APP_NAME = "SoulWhisper POC Demo"
VERSION = "1.0"

# Core Settings
# USE_REAL_BACKEND: 
# True - Connect to real backend API services (iFlytek ASR, Tongyi Emotion Analysis, Zhipu AI Chat)
# False - Use built-in mock data/logic for quick demo
USE_REAL_BACKEND = True

# Module Path (when USE_REAL_BACKEND=True, POC will try to load backend code from this path)
BACKEND_PROJECT_ROOT = "../backend"



# Data and Output Paths
DATA_DIR = "data"
AUDIO_DIR = "audio_samples"
OUTPUT_DIR = "output"
