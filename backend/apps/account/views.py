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
    """User Registration"""
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            sex = data.get('sex', '').strip()
            name = data.get('name', '').strip() or username
            
            # Enhanced validation conditions
            if not username:
                return Response({"error": "Username cannot be empty"}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
            if not password:
                return Response({"error": "Password cannot be empty"}, 
                            status=status.HTTP_400_BAD_REQUEST)
                
            if not sex:
                return Response({"error": "Gender cannot be empty"}, 
                            status=status.HTTP_400_BAD_REQUEST)
                
            if sex not in ['male', 'female', 'other']:
                return Response({"error": "Gender must be 'male', 'female', or 'other'"}, 
                            status=status.HTTP_400_BAD_REQUEST)

            # Verify if username already exists
            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already exists"}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
            # Create user with create_user method
            user = User.objects.create_user(
                username=username,
                name=name,
                sex=sex,
                password=password
            )
            return Response({
                "message": "User registration successful",
                "user": {
                    "username": user.username,
                    "name": user.name,
                    "sex": user.sex
                }
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as ve:
            # Catch ValueError exceptions from create_user
            return Response({"error": str(ve)}, 
                        status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Registration failed: {str(e)}"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """User Login"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required"}, 
                          status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({"error": "Invalid username or password"}, 
                          status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"error": "User is not active"}, 
                          status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)

        user_info = {
            "username": user.username,
            "name": user.name,
            "sex": user.sex,
            "token": token.key
        }
        return Response({"message": "Login successful", "user": user_info},
                      status=status.HTTP_200_OK)

class GetUserInfoView(APIView):
    """Get user information"""
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
