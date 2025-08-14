from django.shortcuts import render, redirect, get_object_or_404
from .models import Comentario
from .forms import ComentarioForm
from apps.noticias.models import Noticia
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages


# Vista para mostrar el detalle de una noticia junto con sus comentarios
def detalle_noticia(request, noticia_id):

    noticia = get_object_or_404(Noticia, pk=noticia_id)
    
    comentarios = Comentario.objects.filter(noticia=noticia).order_by('-fecha')
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)  
        
        if form.is_valid(): 
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.noticia = noticia
            nuevo_comentario.usuario = request.user
            nuevo_comentario.save()
            
            messages.success(request, 'Tu comentario ha sido publicado exitosamente.')
            return redirect('comentario_por_noticia', noticia_id=noticia_id)
    else:
        form = ComentarioForm()  
    
    return render(request, 'comentarios/comentarios.html', {
        'noticia': noticia,
        'comentarios': comentarios,
        'form': form
    })


@login_required  
@require_POST  
def editar_comentario(request, comentario_id):

    try:
        
        comentario = Comentario.objects.get(id=comentario_id, usuario=request.user)
        nuevo_texto = request.POST.get("contenido", "").strip()
        
        if not nuevo_texto:
            return JsonResponse({
                "success": False, 
                "error": "El contenido del comentario no puede estar vacío"
            })
        
        if len(nuevo_texto) < 5:
            return JsonResponse({
                "success": False, 
                "error": "El comentario debe tener al menos 5 caracteres"
            })
        
        if len(nuevo_texto) > 1000:  
            return JsonResponse({
                "success": False, 
                "error": "El comentario no puede exceder los 1000 caracteres"
            })
        
        comentario.contenido = nuevo_texto
        comentario.save()
        
        return JsonResponse({
            "success": True, 
            "contenido": comentario.contenido,
            "mensaje": "Comentario editado exitosamente"
        })
        
    except Comentario.DoesNotExist:
        return JsonResponse({
            "success": False, 
            "error": "Comentario no encontrado o no tienes permisos para editarlo"
        })
    except Exception as e:
        return JsonResponse({
            "success": False, 
            "error": "Error interno del servidor"
        })


@login_required
@require_POST
def eliminar_comentario(request, comentario_id):

    try:
        comentario = Comentario.objects.get(id=comentario_id, usuario=request.user)
        comentario.delete()
        
        return JsonResponse({
            "success": True,
            "mensaje": "Comentario eliminado exitosamente"
        })
        
    except Comentario.DoesNotExist:
        return JsonResponse({
            "success": False, 
            "error": "Comentario no encontrado o no tienes permisos para eliminarlo"
        })
    except Exception as e:
        return JsonResponse({
            "success": False, 
            "error": "Error interno del servidor"
        })