from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        if CustomUser.objects.filter(username=data.get('username')).exists():
            return Response({"error": "Username already exists."}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if CustomUser.objects.filter(email=data.get('email')).exists():
            return Response({"error": "Email already exists."}, 
                          status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            phone_number=data.get('phone_number', ''),
            address=data.get('address', '')
        )

        return Response({"message": "User registered successfully."}, 
                      status=status.HTTP_201_CREATED)
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # 使用 Django 的 authenticate 函数
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({"error": "Invalid credentials."}, 
                          status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"error": "User is not active."}, 
                          status=status.HTTP_401_UNAUTHORIZED)

        # 登录用户
        login(request, user)
        
        # 创建或获取令牌
        token, created = Token.objects.get_or_create(user=user)

        user_info = {
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,
            "address": user.address,
            "token": token.key
        }
        return Response({"message": "Login successful.", "user": user_info}, 
                      status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)

class UpdateUserView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')

        try:
            user = CustomUser.objects.get(username=username)
            
            # 更新所有可能的字段
            if 'email' in data:
                user.email = data.get('email')
            if 'phone_number' in data:
                user.phone_number = data.get('phone_number')
            if 'address' in data:
                user.address = data.get('address')
            if 'avatar' in data:
                user.avatar = data.get('avatar')
            if 'bio' in data:
                user.bio = data.get('bio')
            if 'gender' in data:
                user.gender = data.get('gender')
            if 'birth_date' in data:
                user.birth_date = data.get('birth_date')
            if 'password' in data:
                user.set_password(data.get('password'))

            user.save()
            return Response({"message": "User information updated successfully."}, 
                          status=status.HTTP_200_OK)
                          
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, 
                          status=status.HTTP_404_NOT_FOUND)

class GetUserInfoView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            user_info = {
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number,
                "address": user.address,
                "avatar": user.avatar,
                "bio": user.bio,
                "date_joined": user.date_joined,
                "last_login": user.last_login,
                "gender": user.gender,
                "birth_date": user.birth_date
            }
            return Response(user_info, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        try:
            user = CustomUser.objects.get(username=username)
            if not user.check_password(old_password):
                return Response({"error": "Old password is incorrect."}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password changed successfully."}, 
                          status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, 
                          status=status.HTTP_404_NOT_FOUND)

class DeleteUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            if not user.check_password(password):
                return Response({"error": "Invalid password."}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            user.delete()
            return Response({"message": "User deleted successfully."}, 
                          status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, 
                          status=status.HTTP_404_NOT_FOUND)
