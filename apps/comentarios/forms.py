from django import forms
from .models import Comentario

class comentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nombre','contenido']
