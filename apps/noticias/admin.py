from django.contrib import admin
from apps.noticias.models import Categoria, ImagenNoticia, Noticia

# Register your models here.

# Esta clase es para que se nos permita elegir más de una imagen al crear la noticia.
class ImagenNoticiaInline(admin.TabularInline):
    model = ImagenNoticia 
    extra = 1  # esto muestra 1 campo vacío para subir una imagen por defecto

class NoticiaAdmin(admin.ModelAdmin):
    inlines = [ImagenNoticiaInline]
    list_filter = ('fecha', 'autor', 'categorias')

admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Categoria)