from django import forms
from .models import Comentario

#Definimos un formulario basado en el modelo Comentario
class ComentarioForm(forms.ModelForm):
    class Meta:
        #Definimos que modelo va a utilizar y los campos que vamos a incluir
        model = Comentario
        fields = ["contenido"]
        #Personalizamos el campo contenido
        widgets = {
            "contenido": forms.Textarea(attrs={
                "class": 'form-control',
                "rows": 4,
                "placeholder": "Escribí tu comentario..."}
            ),
        }
        #Etiqueta que se muestra junto al campo de contenido.
        labels = {
            "contenido": 'Mensaje *'
        }
