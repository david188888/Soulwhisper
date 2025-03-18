"""
聊天模块视图
实现与LLM的交互功能
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.utils.llm.get_result import DiaryChat
import json
import logging

logger = logging.getLogger(__name__)

# 聊天会话存储
# 使用内存存储方式，不保存历史记录
active_chat_sessions = {}

class StartChatView(APIView):
    """
    开始日记对话的API视图
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user._id
        diary_content = request.data.get('diary_content', '')
        
        if not diary_content:
            return Response(
                {"error": "日记内容不能为空"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # 创建新的聊天会话
            chat_session = DiaryChat()
            response = chat_session.start_chat(diary_content)
            
            # 保存到内存中
            session_id = str(user_id)
            active_chat_sessions[session_id] = chat_session
            
            return Response({
                "session_id": session_id,
                "response": response
            })
        except Exception as e:
            logger.error(f"启动聊天失败: {str(e)}")
            return Response(
                {"error": "启动聊天失败，请稍后再试"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ChatMessageView(APIView):
    """
    发送消息的API视图
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user_id = request.user._id
        session_id = str(user_id)
        message = request.data.get('message', '')
        
        
        if not message:
            return Response(
                {"error": "消息内容不能为空"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 查找用户的聊天会话
        chat_session = active_chat_sessions.get(session_id)

        if not chat_session:
            return Response(
                {"error": "聊天会话不存在或已过期，请重新开始对话"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            # 发送消息并获取回复
            response = chat_session.chat(message)
            
            return Response({
                "response": response
            })
        except Exception as e:
            logger.error(f"发送消息失败: {str(e)}")
            return Response(
                {"error": "发送消息失败，请稍后再试"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class EndChatView(APIView):
    """
    结束聊天会话的API视图
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user_id = request.user._id
        session_id = str(user_id)
        
        # 删除会话
        if session_id in active_chat_sessions:
            del active_chat_sessions[session_id]
            
        return Response({
            "message": "聊天会话已结束"
        })
