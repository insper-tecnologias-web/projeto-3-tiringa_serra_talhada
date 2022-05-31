from django.db import models
from sqlalchemy import desc

class Card(models.Model):
    rua = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    area = models.IntegerField(default=0)
    quartos = models.IntegerField(default=0)
    vagas = models.IntegerField(default=0)
    banheiros = models.IntegerField(default=0)
    preco = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.id}"