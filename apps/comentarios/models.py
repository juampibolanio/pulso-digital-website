from django.db import models
from django.conf import settings
from apps.noticias.models import Noticia

class Comentario(models.Model):
    noticia = models.ForeignKey(Noticia, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.autor} - {self.noticia.titulo[30]}'