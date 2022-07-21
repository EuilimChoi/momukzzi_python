from dataclasses import dataclass
from pyexpat import model
from wsgiref.validate import validator
from .models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.Serializer):
    userId = serializers.CharField(write_only=True, required=True,validators=[UniqueValidator(queryset=User.objects.all())],)
    nickname = serializers.CharField(write_only=True, required=True,validators=[UniqueValidator(queryset=User.objects.all())],)
    email = serializers.EmailField(required = True, validators=[UniqueValidator(queryset=User.objects.all())],)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password],)
    password2 = serializers.CharField(write_only=True, required=True,)

    class Meta:
        model = User
        fields = ('userId','password','password2','email')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password":"Password fields didn't match."}
            )

        return data
    
    def create(self, data):
        user = User(
            userId = data["userId"],
            password = data["password"],
            email = data["email"],
            nickname = data["nickname"]
        )

class LoginSerializer(serializers.Serializer):
    userId = serializers.CharField(required=True,)
    password = serializers.CharField(write_only=True, required=True,)
