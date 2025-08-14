from django.db import models
from apps.usuarios.models import Usuario

# Create your models here.

class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Noticia(models.Model):
    noticia_id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=85)
    subtitulo = models.CharField(max_length=150)
    contenido = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    categorias = models.ManyToManyField(Categoria)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class ImagenNoticia(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='noticias/noticias_imagenes')

from django.db import models
from apps.usuarios.models import Usuario  # tu modelo de usuarios

# Modelo para guardar mensajes

class ContactMessage(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # quien envía
    asunto = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.asunto}"
