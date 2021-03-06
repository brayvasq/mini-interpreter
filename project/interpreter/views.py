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

parser = Parser()

class UserList(generics.ListAPIView):
    """
        Vista generica que provee solo el método GET
        queryset: objeto del cual se realizarán las consultas
        serializer_class: Clase que parsea las respuestas y las peticiones al formato que se necesite
        permission_classes: Permisos necesarios para acceder a la vista
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        """
        Devuelve el listado de usuarios en caso de que el rol de usuario sea is_reviewer
        :return: Lista de usuarios
        """
        if request.user.is_reviewer:
            user = self.queryset.all()
            return Response(UserSerializer(user,many=True).data)
        else:
            return Response("Access denied!")

class UserCheck(generics.ListAPIView):
    """
        Vista generica que provee solo el método GET
        queryset: objeto del cual se realizarán las consultas
        serializer_class: Clase que parsea las respuestas y las peticiones al formato que se necesite
        permission_classes: Permisos necesarios para acceder a la vista
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permissions = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        """
            Método que verifica el rol de un usuario
            :return: Booleano indicando si es un usuario normal
        """
        if request.user.is_reviewer:
            return Response(data={
                "coder": False
            })
        elif request.user.is_coder:
            return Response(data={
                "coder": True
            })
        else:
            return Response("Access denied!")

class UserDelete(generics.DestroyAPIView):
    """
         Vista generica que provee solo el método DELETE
        queryset: objeto del cual se realizarán las consultas
        serializer_class: Clase que parsea las respuestas y las peticiones al formato que se necesite
        permission_classes: Permisos necesarios para acceder a la vista
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        """
        Método que elimina un usuario en específico dependiendo del valor indicado en la url
        :param request:
        :param args:
        :param kwargs: contiene los parámetros enviados por url
        :return: HTTP_204_NO_CONTENT
        """
        try:
            if request.user.is_reviewer:
                user = self.queryset.get(pk=kwargs["pk"])
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("Access denied!")
        except User.DoesNotExist:
            return Response(
                data={
                    "message": "User with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class SentenceListCreate(generics.ListCreateAPIView):
    """
        Esta vista genérica provee por defecto los métodos GET y POST para las sentencias
        queryset: objeto del cual se realizarán las consultas
        serializer_class: Clase que parsea las respuestas y las peticiones al formato que se necesite
        permission_classes: Permisos necesarios para acceder a la vista
    """
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        """
        Método que ingresa una nueva sentencia a la base de datos
        @validate_request_data valida los datos de la petición
        :param request: posee los datos de la petición, entre ellos, la sentencia de entrada
        :param args:
        :param kwargs:
        :return: Devuelve la sentencia con el resultado despues de ser ejecutada
        """
        if request.user.is_coder:
            input_code = request.data["input_code"]
            global parser
            result = parser.evaluate(input_code)

            sentence = Sentence.objects.create(
                input_code=input_code,
                output_code=result
            )

            return Response(
                data=SentenceSerializer(sentence).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response("Access denied!")


class SentenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        GET sentence/:id/
        PUT sentence/:id/
        DELETE sentence/:id/
        Esta vista genérica provee por defecto los métodos GET,PUT,DELETE para operaciones a detalle de las sentencias
        queryset: objeto del cual se realizarán las consultas
        serializer_class: Clase que parsea las respuestas y las peticiones al formato que se necesite
        permission_classes: Permisos necesarios para acceder a la vista
    """
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Método que obtiene una sentencia en específico dependiendo de un id indicado
        :param request: contiene los datos de la petición
        :param args:
        :param kwargs: contiene los parámetros enviados por url
        :return: Los datos del usuario especificado
        """
        try:
            if request.user.is_coder:
                sentence = self.queryset.get(pk=kwargs["pk"])
                return Response(SentenceSerializer(sentence).data)
            else:
                return Response("Access Denied!")
        except Sentence.DoesNotExist:
            return Response(
                data={
                    "message": "Sentence with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        """
        Método que actualiza los datos de una sentencia en específico dependiendo de un id indicado
        @validate_request_data valida los datos de la petición
        :param request:  contiene los datos de la petición
        :param args:
        :param kwargs: contiene los parámetros enviados por url
        :return: Los nuevos datos del usuario especificado
        """
        try:
            if request.user.is_coder:
                print("Es coder")
                sentence = self.queryset.get(pk=kwargs["pk"])
                serializer = SentenceSerializer()
                data = {}
                data["input_code"] = request.data["input_code"]
                global parser
                data["output_code"] = parser.evaluate(data["input_code"])
                updated_song = serializer.update(sentence, data)
                return Response(SentenceSerializer(updated_song).data)
            else:
                return Response("Access Denied!")
        except Sentence.DoesNotExist:
            return Response(
                data={
                    "message": "Sentence with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        """
        Método que elimina una sentencia en específico dependiendo de un id indicado
        :param request:  contiene los datos de la petición
        :param args:
        :param kwargs: contiene los parámetros enviados por url
        :return: Los nuevos datos del usuario especificado
        """
        try:
            if request.user.is_coder:
                sentence = self.queryset.get(pk=kwargs["pk"])
                sentence.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("Access Denied!")
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
        queryset: objeto del cual se realizarán las consultas
        serializer_class: Clase que parsea las respuestas y las peticiones al formato que se necesite
        permission_classes: Permisos necesarios para acceder a la vista
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Método que loguea a los usuarios
        :param request:  contiene los datos de la petición
        :param args:
        :param kwargs: contiene los parámetros enviados por url
        :return: token JWT para enviar en las peticiones que requieren autenticación
        """
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

            return Response(data={
                "token": serializer.data["token"],
                "is_coder": user.is_coder
            })
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class RegisterUsers(generics.CreateAPIView):
    """
        POST auth/register/
        queryset: objeto del cual se realizarán las consultas
        serializer_class: Clase que parsea las respuestas y las peticiones al formato que se necesite
        permission_classes: Permisos necesarios para acceder a la vista
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """
        Método que registra nuevos usuarios en la plataforma
        :param request:  contiene los datos de la petición
        :param args:
        :param kwargs: contiene los parámetros enviados por url
        :return: HTTP_201_CREATED
        """
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")

        is_coder = True
        is_reviewer = False
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
