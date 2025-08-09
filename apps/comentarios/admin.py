from django.contrib import admin

from apps.comentarios.models import Comentario

# Registramos el modelo Comentario usando un decorador
# Esto asocia la clase ComentarioAdmin con el modelo Comentario para personalizar la interfaz
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    # campos que se mostrarán en la lista principal de admin
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
    #Cambia el nombre de la columna "contenido_corto" a "Comentario"
    contenido_corto.short_description = 'Comentario'