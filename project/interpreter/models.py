from django.db import models

# Create your models here.
class Sentence(models.Model):
    input_code = models.CharField(max_length=100)
    output_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)