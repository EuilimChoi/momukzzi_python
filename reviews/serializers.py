from dataclasses import dataclass
from pyexpat import model
from wsgiref.validate import validator

from attr import field
from .models import Review
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

class ReviewSerializer(serializers.ModelSerializer):
    # shopId_id = serializers.CharField(required=True,)
    # userId_id = serializers.CharField(required = True,allow_blank=True)
    # comment = serializers.CharField(required=True,allow_blank=True)
    # star = serializers.IntegerField(default= 0)
    # def create(self, validated_data):
    #     return Review.objects.create(**validated_data)
    class Meta :
        model = Review
        fields = ['shopId','userId','comment','star']
