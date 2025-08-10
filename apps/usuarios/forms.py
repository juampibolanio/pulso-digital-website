from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'imagen_perfil']

def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id

        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise forms.ValidationError('Este correo electrónico ya está en uso por otro usuario.')
        return email

def clean(self):
        cleaned_data = super().clean()
        required_fields = ['first_name', 'last_name', 'username']

        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, 'Este campo no puede estar vacío.')
