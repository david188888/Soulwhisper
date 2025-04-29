from zhipuai import ZhipuAI
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)
ZHIPUAI_API_KEY = '814313659f8a4194ab4acfd293b0194a.ozUuDGg6qxB38PSR'

client = ZhipuAI(api_key=ZHIPUAI_API_KEY)

def call_llm_api(messages):
    """调用智谱AI接口获取回复"""
    try:
        response = client.chat.completions.create(
            model="glm-4-air",
            messages=messages,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"API调用失败: {str(e)}")
        return None

class DiaryChat:
    def __init__(self):
        self.messages = [{
            "role": "system",
            "content": "You are a warm, empathetic, and insightful mental health companion. Your task is to engage in conversation with users."
        }]

    def start_chat(self, diary_content):
        """开始新的对话"""
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
        """继续对话"""
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

