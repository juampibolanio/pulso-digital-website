from django.shortcuts import render, redirect, get_object_or_404
from .models import Comentario
from .forms import ComentarioForm
from apps.noticias.models import Noticia
from django.contrib.auth.decorators import login_required

def detalle_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    comentarios = Comentario.objects.filter(noticia=noticia).order_by('-fecha')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.usuario = request.user
                comentario.noticia = noticia
                comentario.save()
                return redirect('detalle_noticia', noticia_id=noticia.id)
        else:
            return redirect('login')
    else:
        form = ComentarioForm()

    return render(request, 'comentarios/comentarios.html', {
        'noticia': noticia,
        'comentarios': comentarios,
        'form': form
    })