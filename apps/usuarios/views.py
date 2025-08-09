from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import RegisterForm, PerfilForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Usuario

# Create your views here.

# Registro
def register_view(request):
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('apps.usuarios:login')
    else:
        form = RegisterForm()

    return render(request, 'auth/registro.html', {'form' : form} )

# Login

def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('apps.usuarios:register') # Esto luego debe redireccionar a todas las noticias. Modificar luego
        else:
            messages.error(request, 'Credenciales incorrectas, vuelva a intentarlo.')

    return render(request, 'auth/login.html', )


# Logout

def logout_view(request):

    logout(request)

    return redirect('apps.usuarios:login')

# Ver perfil
@login_required
def ver_perfil(request, id):
    user = Usuario.objects.get(id=id)
    
    
    if user.imagen_perfil and user.imagen_perfil.name:
        imagen_url = user.imagen_perfil.url
    
    context = {
        'user': user,
    }

    return render(request, 'auth/perfil.html', context)

# Editar perfil
@login_required
def editar_perfil(request, id):
    user = Usuario.objects.get(id=id)
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('inicio') 
    else:
        form = PerfilForm(instance=user)
    return render(request, 'auth/editar_perfil.html', {'form': form})

