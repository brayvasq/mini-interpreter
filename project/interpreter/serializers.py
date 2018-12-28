from rest_framework import serializers
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Sentence

class SentenceSerializer(serializers.ModelSerializer):
    """
        Clase que define los elementos o campos para traducir de las sentencias en los formatos indicados
        para las peticiones
    """
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
    """
        Clase que define los elementos o campos para traducir del usuario en los formatos indicados
        para las peticiones
    """
    class Meta:
        model = User
        fields = ("id","username", "email","password","is_coder","is_reviewer")
