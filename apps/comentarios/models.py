from django.db import models
from django.utils import timezone

class Comentario(models.Model):
    nombre = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    noticia = models.ForeignKey('noticias.Noticia', 
                                on_delete=models.CASCADE, 
                                related_name='comentarios')

    def __str__(self):
        return f'Comentario de {self.nombre} en {self.noticia.titulo}'