#!/usr/bin/env python3
"""
ASR (Automatic Speech Recognition) Demo Module.
"""

import os
import json
from pathlib import Path
import sys

class ASRDemo:
    def __init__(self):
        self.transcribe_audio = None
        self.detect_emotion = None
        self.process_audio_backend = None
        try:
            self._setup_real_backend()
        except Exception as e:
            print(f"CRITICAL: Failed to set up real backend. ASR functionality may be impaired. Error: {e}")
                
    def _setup_real_backend(self):
        """Connect to the real backend - Xunfei ASR + Tongyi Emotion API"""
        poc_dir = Path(__file__).resolve().parent.parent
        backend_dir = poc_dir.parent / "backend"
        
        if str(backend_dir) not in sys.path:
            sys.path.insert(0, str(backend_dir))
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')
        
        import django
        django.setup()
        
        from backend.apps.utils.asr.asr_processor import transcribe_audio, detect_emotion, process_audio
        
        self.transcribe_audio = transcribe_audio
        self.detect_emotion = detect_emotion
        self.process_audio_backend = process_audio
        print("✅ Successfully connected to the real backend ASR service")
    def _process_with_real_api(self, audio_path):
        """Call real API - Xunfei ASR + Tongyi Emotion Analysis"""
        if not callable(self.process_audio_backend):
            return {
                "success": False,
                "error": "Real ASR backend not configured or setup failed.",
                "source": "configuration_error"
            }
        try:
            print(f"🎙️ Processing audio using real backend: {Path(audio_path).name}")
            
            result = self.process_audio_backend(audio_path)
            
            if 'error' in result:
                print(f"❌ Backend processing error: {result['error']}")
                return {
                    "success": False,
                    "error": result['error'],
                    "source": "real_backend_error"
                }
            
            print(f"✅ Speech recognition successful: {result.get('text', '')[:50]}...")
            print(f"🎭 Emotion analysis result: {result.get('emotion_type', 'unknown')} (Intensity: {result.get('emotion_intensity', 'N/A')})")
            
            return {
                "success": True,
                "text": result.get('text', ''),
                "emotion_type": result.get('emotion_type', 'neutral'),
                "emotion_intensity": result.get('emotion_intensity', 5),
                "source": "real_backend",
                "audio_file": Path(audio_path).name,
                "api_info": {
                    "asr_api": "讯飞长语音识别API",
                    "emotion_api": "通义语音大模型API"
                }
            }
            
        except Exception as e:
            print(f"⚠️ Error during real backend processing: {str(e)}")            
            return {
                "success": False,
                "error": f"An unexpected error occurred during real backend processing: {str(e)}",
                "source": "real_backend_exception"
            }    
    def process_audio(self, audio_path):
        """Main entry point for audio processing"""
        return self._process_with_real_api(audio_path)
    
    def list_audio_samples(self, audio_dir):
        """List available audio sample files."""
        audio_dir_path = Path(audio_dir)
        if not audio_dir_path.exists() or not audio_dir_path.is_dir():
            print(f"Audio directory not found or is not a directory: {audio_dir}")
            return []
        
        audio_extensions = ['.wav', '.mp3', '.m4a', '.flac']
        audio_files = []
        
        for ext in audio_extensions:
            audio_files.extend(audio_dir_path.glob(f'*{ext}'))
        
        return [str(f) for f in audio_files]
