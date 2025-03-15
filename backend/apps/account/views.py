from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from .models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    """用户注册"""
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            sex = data.get('sex', '').strip()
            name = data.get('name', '').strip() or username
            
            # 加强验证条件
            if not username:
                return Response({"error": "用户名不能为空"}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
            if not password:
                return Response({"error": "密码不能为空"}, 
                            status=status.HTTP_400_BAD_REQUEST)
                
            if not sex:
                return Response({"error": "性别不能为空"}, 
                            status=status.HTTP_400_BAD_REQUEST)
                
            if sex not in ['male', 'female', 'other']:
                return Response({"error": "性别只能是 male、female 或 other"}, 
                            status=status.HTTP_400_BAD_REQUEST)

            # 验证用户名是否已存在
            if User.objects.filter(username=username).exists():
                return Response({"error": "用户名已存在"}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
            # 使用 create_user 创建用户
            user = User.objects.create_user(
                username=username,
                name=name,
                sex=sex,
                password=password
            )
            return Response({
                "message": "用户注册成功",
                "user": {
                    "username": user.username,
                    "name": user.name,
                    "sex": user.sex
                }
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as ve:
            # 捕获 create_user 中的 ValueError 异常
            return Response({"error": str(ve)}, 
                        status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"注册失败: {str(e)}"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """用户登录"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "用户名和密码必填"}, 
                          status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({"error": "用户名或密码错误"}, 
                          status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"error": "用户未激活"}, 
                          status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)

        user_info = {
            "username": user.username,
            "name": user.name,
            "sex": user.sex,
            "token": token.key
        }
        return Response({"message": "登录成功", "user": user_info}, 
                      status=status.HTTP_200_OK)

class GetUserInfoView(APIView):
    """获取用户信息"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        user_info = {
            "username": user.username,
            "name": user.name,
            "sex": user.sex,
            "created_at": user.created_at
        }
        return Response(user_info, status=status.HTTP_200_OK)
