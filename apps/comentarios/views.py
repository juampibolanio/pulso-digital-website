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
    # Obtenemos la noticia o lanzamos error 404 si no existe
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    
    # Obtenemos los comentarios asociados a la noticia, ordenados por fecha descendente
    comentarios = Comentario.objects.filter(noticia=noticia).order_by('-fecha')
    
    # Si el usuario envió el formulario (método POST)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)  # Cargamos el formulario con los datos
        
        if form.is_valid():  # Verificamos validez
            # Creamos la instancia, asociamos la noticia, guardamos el nombre y guardamos el comentario
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.noticia = noticia
            nuevo_comentario.usuario = request.user
            nuevo_comentario.save()
            
            messages.success(request, 'Tu comentario ha sido publicado exitosamente.')
            return redirect('comentario_por_noticia', noticia_id=noticia_id)
    else:
        form = ComentarioForm()  # Si no es POST mostramos el formulario vacío
    
    # Renderizamos el template con la noticia, los comentarios y el formulario
    return render(request, 'comentarios/comentarios.html', {
        'noticia': noticia,
        'comentarios': comentarios,
        'form': form
    })


@login_required  # Solo usuarios autenticados
@require_POST  # Solo método POST
def editar_comentario(request, comentario_id):
    """
    Permite a un usuario autenticado editar su propio comentario.
    Retorna un JSON indicando si fue exitoso o no.
    """
    try:
        # Se obtiene el comentario filtrando por ID y asegurando que pertenezca al usuario autenticado
        comentario = Comentario.objects.get(id=comentario_id, usuario=request.user)
        nuevo_texto = request.POST.get("contenido", "").strip()
        
        # Validar que el texto no esté vacío
        if not nuevo_texto:
            return JsonResponse({
                "success": False, 
                "error": "El contenido del comentario no puede estar vacío"
            })
        
        # Validar longitud mínima y máxima (opcional)
        if len(nuevo_texto) < 5:
            return JsonResponse({
                "success": False, 
                "error": "El comentario debe tener al menos 5 caracteres"
            })
        
        if len(nuevo_texto) > 1000:  # Ajusta según tus necesidades
            return JsonResponse({
                "success": False, 
                "error": "El comentario no puede exceder los 1000 caracteres"
            })
        
        # Si el texto es válido, se actualiza y guarda
        comentario.contenido = nuevo_texto
        comentario.save()
        
        # Retorna JSON con éxito y el nuevo contenido
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
    """
    Permite a un usuario autenticado eliminar su propio comentario.
    Retorna un JSON indicando si fue exitoso o no.
    """
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