from django.shortcuts import render, get_object_or_404, redirect
from .models import Comentario
from .forms import ComentarioForm
from apps.noticias.models import Noticia


def comentarios_por_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    comentarios = noticia.comentarios.all().order_by('-fecha')

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.noticia = noticia
            nuevo_comentario.autor = request.user
            nuevo_comentario.save()
            return redirect('comentario_por_noticia', noticia_id=noticia_id)
    
    else:
        form = ComentarioForm()

    return render(request, 'comentarios/comentarios.html', {'noticia': noticia,
                                                                'comentarios': comentarios, 
                                                                'form': form})