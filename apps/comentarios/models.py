from django.db import models
from django.utils import timezone

from apps.noticias.models import Noticia
from apps.usuarios.models import Usuario

class Comentario(models.Model):
    nombre = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    noticia = models.ForeignKey(Noticia, 
                                on_delete=models.CASCADE, 
                                related_name='comentarios')

    def __str__(self):
        return f'Comentario de {self.nombre} en {self.noticia.titulo}'