from django.contrib import admin

from apps.comentarios.models import Comentario

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'noticia', 'fecha', 'contenido_corto')
    # campos de la barra de busqueda
    search_fields = ('contenido', 'usuario__username', 'noticia__titulo')
    list_filter = ('fecha', 'noticia') #filtros de la barra lateral

    def contenido_corto(self, obj):
        """
        Método personalizado para mostrar una versión corta del contenido del comentario.
        Si el comentario tiene más de 40 caracteres, muestra solo los primeros 40 seguidos de "..."
        """
        return obj.contenido[:40] + "..." if len(obj.contenido) > 40 else obj.contenido
    contenido_corto.short_description = 'Comentario'