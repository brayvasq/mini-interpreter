from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase,APIClient
from rest_framework.views import status
from .models import Sentence
from .serializers import SentenceSerializer
from .parser import Parser
# Create your tests here.

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_song(input_code="",parser=Parser()):
        parser = Parser()
        if input_code != "":
            result = parser.evaluate(input_code)
            Sentence.objects.create(input_code=input_code,output_code=result)

    def setUp(self):
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
        response = self.client.get(
            reverse('sentences-all')
        )
        expected = Sentence.objects.all()
        serialized = SentenceSerializer(expected,many=True)
        self.assertEqual(response.data,serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
