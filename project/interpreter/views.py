from django.shortcuts import render
from .models import Sentence
from .serializers import SentenceSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from .parser import Parser
from .decorators import validate_request_data
# Create your views here.

class SentenceListCreate(generics.ListCreateAPIView):
    """
        Esta vista genérica provee por defecto los
        métodos GET y POST
    """
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
    parser = Parser()

    '''def list(self,request):
        result = self.parser.evaluate('3+3')
        return Response(result)'''

    @validate_request_data
    def post(self, request, *args, **kwargs):
        input_code = request.data["input_code"]
        result = self.parser.evaluate(input_code)

        sentence = Sentence.objects.create(
            input_code = input_code,
            output_code = result
        )

        return Response(
            data = SentenceSerializer(sentence).data,
            status=status.HTTP_201_CREATED
        )

class SentenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        GET sentence/:id/
        PUT sentence/:id/
        DELETE sentence/:id/
    """
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer

    def get(self, request, *args, **kwargs):
        try:
            sentence = self.queryset.get(pk=kwargs["pk"])
            return Response(SentenceSerializer(sentence).data)
        except Sentence.DoesNotExist:
            return Response(
                data={
                    "message": "Sentence with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            sentence = self.queryset.get(pk=kwargs["pk"])
            serializer = SentenceSerializer()
            updated_song = serializer.update(sentence, request.data)
            return Response(SentenceSerializer(updated_song).data)
        except Sentence.DoesNotExist:
            return Response(
                data={
                    "message": "Sentence with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            sentence = self.queryset.get(pk=kwargs["pk"])
            sentence.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Sentence.DoesNotExist:
            return Response(
                data={
                    "message": "Sentence with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )