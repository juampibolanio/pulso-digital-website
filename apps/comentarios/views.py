from django.shortcuts import render, redirect, get_object_or_404
from .models import Comentario
from .forms import ComentarioForm
from apps.noticias.models import Noticia
from django.contrib.auth.decorators import login_required

def detalle_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    comentarios = Comentario.objects.filter(noticia=noticia).order_by('-fecha')

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        form = ComentarioForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.noticia = noticia
            nuevo_comentario.nombre = request.user
            nuevo_comentario.save()
            return redirect('comentario_por_noticia', noticia_id=noticia_id)
    
    else:
        form = ComentarioForm()
        form = ComentarioForm()

    return render(request, 'comentarios/comentarios.html', {
        'noticia': noticia,
        'comentarios': comentarios,
        'form': form
    })