from dataclasses import dataclass
from pyexpat import model
from wsgiref.validate import validator
from .models import Shopinfo,Shopmenu,Shoppic
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

class ShopInfoSerializer(serializers.Serializer):
    shopName = serializers.CharField(required=True,)
    location = serializers.CharField(required = True,allow_blank=True)
    phoneNumber = serializers.CharField(required=True,allow_blank=True)
    def create(self, validated_data):
        return Shopinfo.objects.create(**validated_data)


class ShopPicSerializer(serializers.Serializer):
    shopId_id = serializers.CharField(write_only=True, required=True,)
    URL = serializers.CharField(write_only=True, required=True,)
    def create(self, validated_data):
        return Shoppic.objects.create(**validated_data)    

class ShopMenuSerializer(serializers.Serializer):
    shopId_id = serializers.CharField(write_only=True, required=True,)
    menu = serializers.CharField(write_only=True, required=True,)
    price = serializers.CharField(write_only=True, required=True,)
    def create(self, validated_data):
        return Shopmenu.objects.create(**validated_data)    