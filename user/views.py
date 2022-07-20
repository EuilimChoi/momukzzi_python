
from django.db.models import Q 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer
from rest_framework import status
from django.contrib.auth import authenticate


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
    def post (self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            print(request.data['userId'])
            user = User.objects.filter(userId = request.data['userId'], password = request.data['password']).values()
            print(user[0])
            if user:
                token = Token.objects.create(user=User)
                return Response({"token":token.key}, status=status.HTTP_200_OK)
            return Response({"err":"정보가 이상함"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"err":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    