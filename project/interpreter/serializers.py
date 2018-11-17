from rest_framework import serializers
from .models import Sentence

class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ("id","input_code", "output_code")
        #fields = '__all__'