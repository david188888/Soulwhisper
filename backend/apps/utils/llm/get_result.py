from zhipuai import ZhipuAI
from django.conf import settings
import logging # Add import for logging

logger = logging.getLogger(__name__)
ZHIPUAI_API_KEY = '814313659f8a4194ab4acfd293b0194a.ozUuDGg6qxB38PSR'

client = ZhipuAI(api_key=ZHIPUAI_API_KEY)

def call_llm_api(messages):
    """Call Zhipu AI API to get response"""
    try:
        response = client.chat.completions.create(
            model="glm-4-air",
            messages=messages,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"API call failed: {str(e)}")
        return None

class DiaryChat:
    def __init__(self):
        self.messages = [{
            "role": "system",
            "content": "You are a warm, empathetic, and insightful mental health companion. Your task is to engage in conversation with users."
        }]

    def start_chat(self, diary_content):
        """Start a new conversation"""
        self.messages.append({
            "role": "user",
            "content": f"This is my diary content:{diary_content}"
        })
        
        response = call_llm_api(self.messages)
        if response:
            self.messages.append({
                "role": "assistant",
                "content": response
            })
            return response
        return "Sorry, I can't respond right now, please try again later."

    def chat(self, user_input):
        """Continue the conversation"""
        self.messages.append({
            "role": "user",
            "content": user_input
        })
        
        response = call_llm_api(self.messages)
        if response:
            self.messages.append({
                "role": "assistant",
                "content": response
            })
            return response
        return "Sorry, I can't respond right now, please try again later."

