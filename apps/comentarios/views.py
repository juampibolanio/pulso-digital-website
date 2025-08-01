from django.shortcuts import render, get_object_or_404, redirect
from .models import Comentario
from .forms import ComentarioForm
from noticias.models import Noticia

def detalle_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    comentarios = noticia.comentarios.all().order.by('-fecha')

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.noticia = noticia
            nuevo_comentario.save()
            return redirect('detalle_noticia', noticia_id=noticia.id)
    
    else:
        form = ComentarioForm()

    return render(request, 'comentarios/detalle_noticia.html', {'noticia': noticia,
                                                                'comentarios': comentarios, 
                                                                'form': form})