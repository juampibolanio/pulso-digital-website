from django.db import models
from django.conf import settings
from apps.noticias.models import Noticia

class Comentario(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} comentó en '{self.noticia.titulo}'"