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
            "content": "你是一个温暖、善解人意且富有洞察力的心理陪伴助手。你的任务是与用户围绕他们的日记内容展开对话，包括但不限于提问、帮助排解情绪、提供放松建议和陪聊。保持自然亲切的语气，鼓励用户分享感受，并根据他们的回复逐步深入对话。"
        }]

    def start_chat(self, diary_content):
        """开始新的对话"""
        self.messages.append({
            "role": "user",
            "content": f"这是我今天的日记：{diary_content}"
        })
        
        response = call_llm_api(self.messages)
        if response:
            self.messages.append({
                "role": "assistant",
                "content": response
            })
            return response
        return "很抱歉，我现在无法回应，请稍后再试。"

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
        return "很抱歉，我现在无法回应，请稍后再试。"

