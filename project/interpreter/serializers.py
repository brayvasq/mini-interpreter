from rest_framework import serializers
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Sentence

class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ("id","input_code", "output_code")
        #fields = '__all__'

class TokenSerializaer(serializers.Serializer):
    """
        Este clase es para serializar el token
    """
    token = serializers.CharField(max_length=255)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email","password","is_coder","is_reviewer")
