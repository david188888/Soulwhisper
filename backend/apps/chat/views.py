"""
Chat module views
Implements interaction functionality with LLM
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.utils.llm.get_result import DiaryChat
import logging

logger = logging.getLogger(__name__)

# Chat session storage
# Using in-memory storage method, not saving history
active_chat_sessions = {}

class StartChatView(APIView):
    """
    API view for starting a diary conversation
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user._id
        diary_content = request.data.get('diary_content', '')
        
        if not diary_content:
            return Response(
                {"error": "Diary content cannot be empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Create a new chat session
            chat_session = DiaryChat()
            response = chat_session.start_chat(diary_content)
            
            # Save to memory
            session_id = str(user_id)
            active_chat_sessions[session_id] = chat_session
            
            return Response({
                "session_id": session_id,
                "response": response
            })
        except Exception as e:
            logger.error(f"Failed to start chat: {str(e)}")
            return Response(
                {"error": "Failed to start chat, please try again later"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ChatMessageView(APIView):
    """
    API view for sending messages
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user_id = request.user._id
        session_id = str(user_id)
        message = request.data.get('message', '')
        
        
        if not message:
            return Response(
                {"error": "Message content cannot be empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find user's chat session
        chat_session = active_chat_sessions.get(session_id)

        if not chat_session:
            return Response(
                {"error": "Chat session does not exist or has expired, please restart the conversation"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            # Send message and get response
            response = chat_session.chat(message)
            
            return Response({
                "response": response
            })
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}")
            return Response(
                {"error": "Failed to send message, please try again later"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class EndChatView(APIView):
    """
    API view for ending a chat session
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user_id = request.user._id
        session_id = str(user_id)
        
        # Delete session
        if session_id in active_chat_sessions:
            del active_chat_sessions[session_id]

        return Response({
            "message": "Chat session has ended"
        })
