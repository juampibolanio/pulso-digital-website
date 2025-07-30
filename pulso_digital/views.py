from django.shortcuts import render

# acá defino la página principal. ('')
def inicio(request):
    return render(request, 'index.html')