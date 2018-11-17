from django.shortcuts import render
from .models import Sentence
from .serializers import SentenceSerializer
from rest_framework import generics
from rest_framework.response import Response
from .parser import Parser
# Create your views here.

class SentenceListCreate(generics.ListCreateAPIView):
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
    parser = Parser()

    def list(self,request):
        result = self.parser.evaluate('3+3')
        return Response(result)

    def post(self, request, *args, **kwargs):
        input_code = request.data["input_code"]
        result = self.parser.evaluate(input_code)
        return Response(result)
