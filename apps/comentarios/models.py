from django.db import models
from django.utils import timezone

from apps.noticias.models import Noticia
from apps.usuarios.models import Usuario

# Modelo que representa un comentario hecho por un usuario en una noticia.
class Comentario(models.Model):
    # Cuando el usuario se borra, tambien se borran los comentarios
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    # si se borra la noticia, se borran los comentarios.
    noticia = models.ForeignKey(Noticia, 
                                on_delete=models.CASCADE, 
                                related_name='comentarios')

    def __str__(self):
        """
        Representación legible del comentario.
        Muestra el usuario y una parte del título de la noticia.
        """
        return f'{self.usuario} - {self.noticia.titulo[:30]}'
    
    def getName(self):
        """
        Devuelve el nombre completo del usuario si está disponible.
        Si no, muestra solo el nombre o el username.
        """
        if self.usuario.first_name and self.usuario.last_name:
            return f"{self.usuario.first_name} {self.usuario.last_name}"
        elif self.usuario.first_name:
            return self.usuario.first_name
        else:
            return self.usuario.username
    
    def getUsername(self):
        """Devuelve el username del usuario"""
        return self.usuario.username
    
    def getUserImage(self):
        """Devuelve la imagen de perfil del usuario o None si no tiene"""
        if hasattr(self.usuario, 'imagen_perfil') and self.usuario.imagen_perfil:
            return self.usuario.imagen_perfil.url
        return None
    
    class Meta:
        ordering = ['-fecha']  # Ordena por fecha descendente por defecto
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"