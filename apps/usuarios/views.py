from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout

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