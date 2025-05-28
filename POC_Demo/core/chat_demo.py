#!/usr/bin/env python3
"""
AI Chat Demo Module.
Provides intelligent conversation based on emotional state.
"""

import random
import json
import os
import sys
from pathlib import Path

class ChatDemo:    
    def __init__(self):
        self.conversation_history = []
        self.call_llm_api = None
        self.emotion_context = None

        self.SYSTEM_PROMPT_CHAT = """You are a professional psychological companion AI assistant named SoulWhisper. Your tasks are:
                                    1. Listen to the user's emotional expressions.
                                    2. Provide warmth, understanding, and support.
                                    3. Respond appropriately based on the user's emotional state.
                                    4. Offer positive suggestions and encouragement when appropriate.

                                    Please respond in a warm and understanding tone, not exceeding 200 words."""

        self.SYSTEM_PROMPT_SUMMARY = """You are a conversation analysis assistant. Based on the following conversation history, please generate a concise summary including the main topics discussed, the user's emotional trend (if reflected in the conversation), and the overall atmosphere of the conversation. The summary should be objective and not exceed 150 words."""
        
        try:
            self._setup_real_backend()
        except Exception as e:
            print(f"CRITICAL: Failed to set up real backend for Chat. Chat functionality may be impaired. Error: {e}")
            print("💡 Will use mock chat functionality as fallback.")
            self._setup_mock_backend()
                
    def _setup_real_backend(self):
        """Connect to the real backend - Zhipu AI Chat Service"""
        poc_dir = Path(__file__).resolve().parent.parent
        backend_dir = poc_dir.parent / "backend"
        if str(backend_dir) not in sys.path:
            sys.path.insert(0, str(backend_dir))
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')
        try:
            import django
            django.setup()
        except ImportError as e:
            print(f"Error importing Django: {e}. Ensure Django is installed and configured.")
            raise
        
        from backend.apps.utils.llm.get_result import call_llm_api
        
        self.call_llm_api = call_llm_api
        print("✅ Successfully connected to the real backend AI chat service")
        
    def _setup_mock_backend(self):
        """Setup mock chat functionality when real backend is not available"""
        self.call_llm_api = None
        print("🔧 Using mock chat functionality")
        
    def _chat_with_mock_ai(self, emotion_context, user_text):
        """Mock chat functionality for demo purposes"""
        # 模拟情感感知回复
        emotion_responses = {
            'happy': ["I'm so glad to hear you're feeling positive! 😊", "Your happiness is wonderful to see!", "That sounds fantastic!"],
            'sad': ["I understand you're going through a difficult time. I'm here for you. 💙", "It's okay to feel sad sometimes. Would you like to talk about it?", "I'm sorry you're feeling this way."],
            'angry': ["I can sense your frustration. Let's work through this together.", "It's natural to feel angry sometimes. Take a deep breath.", "I hear your anger. What's troubling you?"],
            'anxious': ["I understand you're feeling worried. Let's take this one step at a time.", "Anxiety can be overwhelming. I'm here to support you.", "Your concerns are valid. Let's talk through them."],
            'excited': ["Your excitement is contagious! Tell me more!", "I love your enthusiasm!", "That's amazing! I'm excited for you too!"],
            'neutral': ["I'm here to listen and support you.", "How are you feeling today?", "Tell me what's on your mind."]
        }
        
        # 根据情感上下文选择合适的回复
        if emotion_context and isinstance(emotion_context, dict):
            emotion_label = emotion_context.get('emotion_label', 'neutral').lower()
            if emotion_label in emotion_responses:
                response_list = emotion_responses[emotion_label]
            else:
                response_list = emotion_responses['neutral']
        else:
            response_list = emotion_responses['neutral']
        
        # 选择一个随机回复
        ai_response = random.choice(response_list)
        
        # 记录对话历史
        self.conversation_history.append({"role": "user", "content": user_text})
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        
        return {
            "success": True,
            "ai_response": ai_response,
            "source": "mock_chat",
            "emotion_context": emotion_context,
            "conversation_turns": len(self.conversation_history) // 2
        }
    def _chat_with_real_backend(self, emotion_context, user_text):
        """Call real API - Zhipu AI GLM-4-Air Chat"""
        if not callable(self.call_llm_api):
            print("❌ Real backend for Chat is not configured or setup failed.")
            return {
                "success": False,
                "error": "Real Chat backend not configured or setup failed.",
                "source": "configuration_error"
            }        
        try:
            emotion_for_log = 'N/A'
            if emotion_context and isinstance(emotion_context, dict):
                emotion_for_log = emotion_context.get('emotion_label', emotion_context.get('primary_emotion', 'N/A'))
            print(f"💬 Starting chat with real backend. Emotion context: {emotion_for_log}")            
            messages = [
                {"role": "system", "content": self.SYSTEM_PROMPT_CHAT}
            ]
            
            if emotion_context and isinstance(emotion_context, dict):
                emotion_info = f"用户当前情感状态: {emotion_context.get('emotion_label', '未知')}"
                if 'confidence' in emotion_context:
                    emotion_info += f", 置信度: {emotion_context['confidence']}"
                if 'intensity' in emotion_context:
                    emotion_info += f", 强度: {emotion_context['intensity']}%"
                messages[0]["content"] += f"\n\n{emotion_info}"
            
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": user_text})            
            ai_response_raw = self.call_llm_api(messages)

            if ai_response_raw:
                ai_response = ai_response_raw 
                self.conversation_history.append({"role": "user", "content": user_text})
                self.conversation_history.append({"role": "assistant", "content": ai_response})
                print(f"✅ Real backend chat response received.")
                return {
                    "success": True,
                    "ai_response": ai_response,
                    "source": "real_backend_chatllm",
                    "emotion_context": emotion_context,
                    "conversation_turns": len(self.conversation_history) // 2
                }
            else:
                print("❌ Real backend chat API call failed or returned empty response.")
                return {
                    "success": False,
                    "error": "Real backend chat API call failed or returned empty response.",
                    "source": "real_backend_chatllm_api_error"
                }
        except Exception as e:
            print(f"⚠️ Error during real backend chat: {str(e)}")
            return {
                "success": False,
                "error": f"An unexpected error occurred during real backend chat: {str(e)}",
                "source": "real_backend_chatllm_exception"
            }
    
    # ================== Emotion Context Management Methods ==================
    def update_emotion_context(self, new_emotion_context):
        """Update the global emotion context for ongoing conversation."""
        self.emotion_context = new_emotion_context
        print(f"🔄 Emotion context updated: {new_emotion_context.get('emotion_label', 'Unknown') if new_emotion_context else 'None'}")
    
    def get_emotion_context(self):
        """Get the current emotion context."""
        return self.emotion_context
    
    def reset_emotion_context(self):
        """Reset emotion context to None."""
        self.emotion_context = None
        print("🔄 Emotion context reset.")

    # ================== Conversation Management Methods ==================
    def start_conversation(self, emotion_context=None, user_text="Hello"):
        """Main entry point for starting a new AI conversation."""
        self.conversation_history = []
        self.emotion_context = emotion_context
        if callable(self.call_llm_api):
            return self._chat_with_real_backend(emotion_context if emotion_context else {}, user_text)
        else:
            print("🤖 Real backend not available. Using mock chat functionality.")
            return self._chat_with_mock_ai(emotion_context, user_text)
    def continue_conversation(self, user_input):
        """Main entry point for continuing a conversation."""
        if not user_input or not user_input.strip():
            return {"success": False, "error": "User input cannot be empty.", "ai_response": "Please say something."}
        
        if callable(self.call_llm_api):
            return self._continue_conversation_with_real_backend(user_input)
        else:
            print("🤖 Real backend not available. Using mock chat functionality.")
            return self._continue_conversation_with_mock_ai(user_input)
    def _continue_conversation_with_real_backend(self, user_input):
        """Call real API - Zhipu AI to continue chat"""
        return self._chat_with_real_backend(emotion_context=self.emotion_context, user_text=user_input)

    def _continue_conversation_with_mock_ai(self, user_input):
        """Continue conversation with mock AI"""
        return self._chat_with_mock_ai(self.emotion_context, user_input)
    def get_conversation_summary(self):
        """Get a summary of the current conversation."""
        if not self.conversation_history:
            return {"success": False, "summary": "No conversation history to summarize."}

        if callable(self.call_llm_api):
            return self._get_summary_with_real_backend()
        else:
            print("🤖 Real backend not available. Using mock summary functionality.")
            return self._get_summary_with_mock_ai()
    def _get_summary_with_real_backend(self):
        """Get summary using real backend LLM."""
        if not callable(self.call_llm_api):
             return {"success": False, "summary": "LLM for summary not configured.", "source": "configuration_error"}
        try:
            print("📝 Requesting conversation summary from real backend...")
            messages = [
                {"role": "system", "content": self.SYSTEM_PROMPT_SUMMARY},
                {"role": "user", "content": json.dumps(self.conversation_history)}
            ]
            summary = self.call_llm_api(messages)
            if summary:
                print("✅ Summary received from backend.")
                return {"success": True, "summary": summary, "source": "real_backend_summaryllm"}
            else:
                print("❌ Summary generation by backend failed or returned empty.")
                return {"success": False, "summary": "Failed to generate summary from backend.", "source": "real_backend_summaryllm_api_error"}
        except Exception as e:
            print(f"⚠️ Error during summary generation with real backend: {str(e)}")
            return {"success": False, "summary": f"Error generating summary: {str(e)}", "source": "real_backend_summaryllm_exception"}

    def _get_summary_with_mock_ai(self):
        """Generate mock conversation summary"""
        if not self.conversation_history:
            return {"success": False, "summary": "No conversation to summarize."}
        
        # Simple mock summary based on conversation length and emotion context
        turns = len(self.conversation_history) // 2
        emotion_text = ""
        if self.emotion_context and isinstance(self.emotion_context, dict):
            emotion_label = self.emotion_context.get('emotion_label', 'neutral')
            emotion_text = f" The user showed signs of {emotion_label} emotion during the conversation."
        
        mock_summary = f"This was a {turns}-turn conversation between the user and AI assistant.{emotion_text} The AI provided supportive responses and engaged empathetically with the user's messages."
        
        return {
            "success": True,
            "summary": mock_summary,
            "source": "mock_summary",
            "conversation_turns": turns
        }


