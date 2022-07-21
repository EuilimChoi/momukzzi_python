
from django.db.models import Q 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import jwt


# Create your views here.

from .serializers import RegisterSerializer

class RegisterView(APIView):
    def post (self, request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    model = User

    def post (self, request):
        user1 = User(userId="chlcui1324")
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            userinfo = User.objects.filter(userId = request.data['userId'], password = request.data['password']).values()
            if userinfo:
                token = jwt.encode({"userId":request.data["userId"]}, "1234", algorithm="HS256")
                return Response({"token":token, "userId":request.data["userId"]}, status=status.HTTP_200_OK)

            return Response({"err":"정보가 이상함"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"err":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
