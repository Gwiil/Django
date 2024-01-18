from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.
LISTA_CATEGORIA = (
    ("ANALISES", "Análises"), #(COMO VAI APARECER NO BANCO , COMO VAI APARECER PRO USUARIO
    ("PROGRAMACAO", "Programação"),
    ("APRESENTACAO", "Apresentação"),
    ("FICCAO", "Ficção"),
    ("FANTASIA", "Fantasia"),
    ("OUTROS", "Outros"),
)
# criar filmes
class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    thumb = models.ImageField(upload_to='thumb_filmes')
    descricao = models.TextField(max_length=1000)
    categoria = models.CharField(max_length=20, choices=LISTA_CATEGORIA)
    visualizacoes = models.IntegerField(default=0)
    data_de_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo


#criar episodios
class Episodio(models.Model):
    filme = models.ForeignKey("Filme", related_name='episodios', on_delete=models.CASCADE)      #Chave estrangeira para conectar os bancos
    titulo = models.CharField(max_length=100)
    video = models.URLField()

    def __str__(self):
        return self.filme.titulo +" - "+ self.titulo


#criar usuarios

class Usuario(AbstractUser):
    filmes_vistos = models.ManyToManyField("Filme")
