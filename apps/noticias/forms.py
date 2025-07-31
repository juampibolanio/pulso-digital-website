from django import forms
from .models import Noticia, ImagenNoticia

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'subtitulo', 'contenido', 'categorias', 'autor']

class NoticiaImagenForm(forms.ModelForm):

    class Meta:
        model = ImagenNoticia
        fields = ['imagen']