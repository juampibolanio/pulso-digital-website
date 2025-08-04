from django import forms
from .models import Comentario


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["contenido"]
        widgets = {
            "contenido": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Escribí tu comentario..."}
            ),
        }
