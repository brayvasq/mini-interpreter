from django.test import TestCase
import json
from django.urls import reverse
#from django.contrib.auth.models import User
from rest_framework.test import APITestCase,APIClient
from rest_framework.views import status
from .models import Sentence
from .serializers import SentenceSerializer
from .parser import Parser
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your tests here.

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_song(input_code="",parser=Parser()):
        parser = Parser()
        if input_code != "":
            result = parser.evaluate(input_code)
            Sentence.objects.create(input_code=input_code,output_code=result)

    def login_user(self,username="",password=""):
        url = reverse('auth-login')

        return self.client.post(
            url,
            data= json.dumps({
                "username":username,
                "password":password
            }),
            content_type="application/json"
        )

    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse('create-token'),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token

    def setUp(self):
        # Creando un usuario admin
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user"
        )

        # Test del interprete
        parser = Parser()
        self.create_song('3+3',parser)
        self.create_song('3',parser)
        self.create_song('x=1',parser)


class GetAllCodeTest(BaseViewTest):
    def test_get_all_code(self):
        """
            Este método se verifica que todos los items que se agregaron
            en el setUp existan en la base de datos y los devuelva cuando
            se hace una petición GET
        """
        self.login_client('test_user', 'testing')
        response = self.client.get(
            reverse('sentences-all')
        )
        expected = Sentence.objects.all()
        serialized = SentenceSerializer(expected,many=True)
        self.assertEqual(response.data,serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthLoginUserTest(BaseViewTest):
    """
        Pruebas para el login de los usuarios
    """
    def test_login_user_valid(self):
        # Haciendo Test con credenciales validas
        response = self.login_user("test_user", "testing")
        # Assert si existe un token en la respuesta
        self.assertIn("token",response.data)
        # Assert si el codigo de respuesta es 200
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        # Haciendo Test ccon credenciales invalidas
        response = self.login_user("anonymus","pass")
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
