from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nome = models.CharField(max_length = 255)

    def __str__(self):
        return self.nome

class Contato(models.Model):
    nome = models.CharField(max_length = 255)
    sobrenome = models.CharField(max_length = 255, blank = True) #blank = True, para deixar campo como opcional
    telefone = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255, blank = True)
    data_criacao = models.DateTimeField(default=timezone.now)
    descricao = models.CharField(max_length = 255, blank = True)
    categoria = models.ForeignKey(Categoria, on_delete = models.DO_NOTHING)
    mostrar = models.BooleanField(default= True)
    foto = models.ImageField(blank = True, upload_to = 'fotos/%Y/%m/%d')
   
    def __str__(self):
            return self.nome



