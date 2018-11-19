from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_coder = models.BooleanField(default=False)
    is_reviewer = models.BooleanField(default=False)

    #    swappable = 'AUTH_USER_MODEL'

class Sentence(models.Model):
    # Código de entrada
    input_code = models.CharField(max_length=100)
    # Resultado arrojado por el parser
    output_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} => {}".format(self.input_code, self.output_code)
