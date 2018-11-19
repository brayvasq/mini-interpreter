from django.shortcuts import render
from .models import Sentence
from .serializers import SentenceSerializer, TokenSerializaer, UserSerializer
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,get_user_model
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from .parser import Parser
from .decorators import validate_request_data

# Create your views here.
User = get_user_model()
# Creando la configuración de JWT
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        if request.user.is_reviewer:
            user = self.queryset.all()
            return Response(UserSerializer(user,many=True).data)
        else:
            return Response("Access denied!")

class SentenceListCreate(generics.ListCreateAPIView):
    """
        Esta vista genérica provee por defecto los
        métodos GET y POST
    """
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser = Parser()

    '''def list(self,request):
        result = self.parser.evaluate('3+3')
        return Response(result)'''

    @validate_request_data
    def post(self, request, *args, **kwargs):
        input_code = request.data["input_code"]
        result = self.parser.evaluate(input_code)

        sentence = Sentence.objects.create(
            input_code=input_code,
            output_code=result
        )

        return Response(
            data=SentenceSerializer(sentence).data,
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
    permission_classes = (permissions.IsAuthenticated,)

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


class LoginView(generics.CreateAPIView):
    """
        View para el método POST auth/login
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # El método login guarda el ID del user en la session
            # usando Django session framework
            login(request, user)
            serializer = TokenSerializaer(data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )
            })
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterUsers(generics.CreateAPIView):
    """
        POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        is_coder = True if request.data.get("is_coder","") == 'true' else False
        is_reviewer = True if request.data.get("is_reviewer","") == 'true' else False

        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email are required!"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email,is_coder=is_coder,is_reviewer=is_reviewer
        )
        return Response(status=status.HTTP_201_CREATED)
