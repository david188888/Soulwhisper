#!/usr/bin/env python3
"""
Emotion analysis demo module.
Analyzes the sentiment tendency and intensity of text.
"""

import json
import random
import os
from pathlib import Path

class EmotionDemo:
    EMOTION_LABELS = {
        "happy": "Happy",
        "sad": "Sad",
        "angry": "Angry",
        "fear": "Fear", 
        "neutral": "Neutral"
    }
    
    def __init__(self):
        self.call_llm_api = None
        
        try:
            self._setup_real_backend()
        except Exception as e:
            print(f"CRITICAL: Failed to set up real backend. Emotion analysis may not function correctly. Error: {e}")

    def _setup_real_backend(self):
        """Connect to the real backend - Zhipu AI Emotion Analysis"""
        import sys
        from pathlib import Path
        
        poc_dir = Path(__file__).parent.parent
        backend_dir = poc_dir.parent / "backend"
        
        if str(backend_dir) not in sys.path:
            sys.path.insert(0, str(backend_dir))
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')
        
        import django
        django.setup()
        
        from backend.apps.utils.llm.get_result import call_llm_api
        
        self.call_llm_api = call_llm_api
        print("✅ Successfully connected to the real backend emotion analysis service")
    def _analyze_with_real_backend(self, text):
        """Call real API - Zhipu AI GLM-4-Air Emotion Analysis"""
        if not hasattr(self, 'call_llm_api') or not callable(self.call_llm_api):
            return {
                "success": False,
                "error": "Real backend not configured or setup failed.",
                "source": "configuration_error"
            }
        try:
            print(f"📝 Analyzing text emotion using real backend: {text[:50]}...")
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a professional emotion analysis assistant. Please analyze the sentiment of the user's text and return the results in JSON format."
                },
                {
                    "role": "user", 
                    "content": f"""Please analyze the sentiment of the following text:
                    
                "{text}"

                Please select a primary emotion type from the following options: happy, sad, angry, neutral, fear

                And provide an emotion intensity score from 1-10.

                Please return in JSON format, including the following fields:
                - primary_emotion: Primary emotion type
                - emotion_label: Emotion label
                - confidence: Confidence (0-1)
                - intensity: Emotion intensity (1-10)
                - analysis: Brief analysis"""
                }
            ]
            
            response = self.call_llm_api(messages)
            
            if response:
                print(f"✅ Backend emotion analysis completed")
                
                import json
                import re 
                
                try:
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        result_json = json.loads(json_match.group())
                        
                        primary_emotion = result_json.get('primary_emotion', 'neutral')
                        if primary_emotion not in ['happy', 'sad', 'angry', 'neutral', 'fear']:
                            primary_emotion = 'neutral'
                            
                        intensity = result_json.get('intensity', 5)
                        if not isinstance(intensity, (int, float)) or not (1 <= intensity <= 10):
                            intensity = 5
                            
                        confidence = result_json.get('confidence', 0.8)
                        if not isinstance(confidence, (int, float)) or not (0 <= confidence <= 1):
                            confidence = 0.8
                        
                        return {
                            "success": True,
                            "primary_emotion": primary_emotion,
                            "emotion_label": self.EMOTION_LABELS.get(primary_emotion, "Unknown"),
                            "confidence": round(confidence, 2),
                            "intensity": round(intensity, 2),
                            "text_length": len(text),
                            "analysis": result_json.get('analysis', 'Deep learning-based emotion analysis'),
                            "source": "real_backend_llm",
                            "api_info": {
                                "model": "智谱AI GLM-4-Air",
                                "provider": "智谱AI"
                            }
                        }
                    else:
                        print(f"⚠️ No JSON found in backend response.")
                        return {
                            "success": False,
                            "error": "No JSON found in backend response.",
                            "source": "real_backend_llm_parsing_error",
                            "raw_response": response[:500]
                        }
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"⚠️ JSON parsing failed: {e}")
                    return {
                        "success": False,
                        "error": "JSON parsing failed",
                        "details": str(e),
                        "source": "real_backend_llm_parsing_error",
                        "raw_response": response[:500]
                    }
            else:
                print("❌ Backend API call failed or returned empty response.")
                return {
                    "success": False,
                    "error": "Backend API call failed or returned empty response.",
                    "source": "real_backend_llm_api_error"
                }

        except Exception as e:
            print(f"⚠️ Error during real backend analysis: {str(e)}")
            return {
                "success": False,
                "error": f"An unexpected error occurred during real backend analysis: {str(e)}",
                "source": "real_backend_llm_exception"
            }    
    def analyze_emotion(self, text):
        """Main entry point for emotion analysis"""
        return self._analyze_with_real_backend(text)
    
    def get_emotion_advice(self, emotion_result):
        """Provide advice based on emotion analysis results"""
        emotion = emotion_result.get("primary_emotion", "neutral")
        
        advice_map = {
            "happy": "Glad to see you're in a good mood! Maintain this positive attitude and try sharing this happiness with those around you.",
            "sad": "It seems you're a bit sad right now. Remember this emotion is temporary. Try doing something relaxing, like listening to music or taking a walk.",
            "angry": "Sensing some anger. Take a deep breath and try releasing these negative emotions through exercise or writing.",
            "fear": "You seem a bit worried or anxious. Try to analyze the specific concerns; most fears are more severe in thought than in reality.",
            "neutral": "Your emotions are quite stable, which is good. Try doing something interesting to add some color to your life."
        }
        
        return advice_map.get(emotion, "Maintain inner peace; every day is a new beginning.")
