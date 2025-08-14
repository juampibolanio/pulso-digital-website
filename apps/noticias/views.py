from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from apps.comentarios.forms import ComentarioForm
from apps.comentarios.models import Comentario
from django.db.models import Count
from .models import Categoria, ImagenNoticia, Noticia, ContactMessage
from django.http import JsonResponse
from .forms import NoticiaForm
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test

#Listar todas las categorías
def categorias():
    categorias = Categoria.objects.all()
    return categorias

# Filtro para noticias por categoria
def categoria(request, categoria_id=None):
    todas_las_categorias = Categoria.objects.all()
    noticias_trending = Noticia.objects.all()[:5]

    if categoria_id:
        categoria_seleccionada = get_object_or_404(Categoria, pk=categoria_id)
        noticias = Noticia.objects.filter(categorias=categoria_seleccionada)
    else:
        categoria_seleccionada = None
        noticias = Noticia.objects.all()

    # Anotar cantidad de comentarios
    noticias = noticias.annotate(num_comentarios=Count('comentarios'))

    # Filtros por orden
    orden = request.GET.get('orden', '')
    sentido = request.GET.get('sentido', 'desc')

    if orden == 'comentarios':
        noticias = noticias.order_by('num_comentarios' if sentido == 'asc' else '-num_comentarios')
    elif orden == 'fecha':
        noticias = noticias.order_by('fecha' if sentido == 'asc' else '-fecha')
    else:
        noticias = noticias.order_by('-noticia_id')

    paginator = Paginator(noticias, 12)
    num_pagina = request.GET.get('page')
    pagina_noticia = paginator.get_page(num_pagina)

    context = {
        'noticias': pagina_noticia,
        'todas_las_categorias': todas_las_categorias,
        'categoria_seleccionada': categoria_seleccionada,
        'total_noticias': noticias.count(),
        'noticias_trending': noticias_trending
    }

    return render(request, 'noticias/categoria.html', context)

# Listar todas las noticias
def noticias(request):
    noticias = Noticia.objects.all()
    categorias_list = Categoria.objects.all()
    noticias_trending = Noticia.objects.all()[:5]

    # Filtro por categoría
    categoria_nombre = request.GET.get('categoria', '').strip()
    if categoria_nombre:
        noticias = noticias.filter(categorias__nombre__icontains=categoria_nombre)

    # Anotar cantidad de comentarios
    noticias = noticias.annotate(num_comentarios=Count('comentarios'))

    # Filtros por orden
    orden = request.GET.get('orden', '')  
    sentido = request.GET.get('sentido', 'desc')  

    if orden == 'comentarios':
        noticias = noticias.order_by('num_comentarios' if sentido == 'asc' else '-num_comentarios')
    elif orden == 'fecha':
        noticias = noticias.order_by('fecha' if sentido == 'asc' else '-fecha')
    else:
        noticias = noticias.order_by('-noticia_id')  

    # Paginación
    paginator = Paginator(noticias, 6)
    num_pagina = request.GET.get('page')
    pagina_noticia = paginator.get_page(num_pagina)

    context = {
        "noticias": pagina_noticia,
        "categorias": categorias_list,
        "todas_las_categorias": categorias_list,
        "noticias_trending": noticias_trending
    }

    return render(request, 'noticias/noticias.html', context)

# Detalle de la noticia
def detalle_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    comentarios = Comentario.objects.filter(noticia=noticia).order_by('-fecha')
    imagenes = noticia.imagenes.all()
    todas_las_categorias = categorias()
    noticias_trending = Noticia.objects.all()[:5]

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                nuevo_comentario = form.save(commit=False)
                nuevo_comentario.usuario = request.user
                nuevo_comentario.noticia = noticia
                nuevo_comentario.save()
                return redirect('apps.noticias:detalle_noticia', noticia_id=noticia_id)
        else:
            return redirect('apps.usuarios:login')
    else:
        form = ComentarioForm()

    context = {
        'detalle': noticia,
        'comentarios': comentarios,
        'form': form,
        'imagen': imagenes,
        'todas_las_categorias': todas_las_categorias,
        'noticias_trending' : noticias_trending
    }

    return render(request, 'noticias/detalle_noticia.html', context )

# Crear noticia
@permission_required('noticias.add_noticia', raise_exception=True)
def crear_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST)
        imagenes = request.FILES.getlist('imagenes')

        if form.is_valid():
            nueva_noticia = form.save()

            for imagen in imagenes:
                ImagenNoticia.objects.create(noticia=nueva_noticia, imagen=imagen)

            return redirect('apps.noticias:todas_las_noticias')  
    else:
        form = NoticiaForm(initial={'autor': request.user})

    context = {
        "form": form
    }

    return render(request, 'noticias/crear_noticia.html', context)

# Editar una noticia por su ID
@permission_required('noticias.change_noticia', raise_exception=True)
def editar_noticia(request, noticia_id):
    noticia = Noticia.objects.get(noticia_id=noticia_id)

    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        imagenes_nuevas = request.FILES.getlist('imagenes')
        imagenes_a_eliminar = request.POST.getlist('eliminar_imagenes')

        if form.is_valid():
            noticia_editada = form.save()

            # para guardar imágenes nuevas
            for imagen in imagenes_nuevas:
                ImagenNoticia.objects.create(noticia=noticia_editada, imagen=imagen)

            # para eliminar las imagenes seleccionadas
            for imagen_id in imagenes_a_eliminar:
                try:
                    imagen = ImagenNoticia.objects.get(id=imagen_id, noticia=noticia)
                    imagen.imagen.delete()  # esto para para q la imagen tambien se borre de la carpeta media root q configuramos.
                    imagen.delete()
                except ImagenNoticia.DoesNotExist:
                    pass

            return redirect("apps.noticias:detalle_noticia", noticia_id=noticia.noticia_id)
    else:
        form = NoticiaForm(instance=noticia)

    context = {
        "form": form,
        "noticia": noticia
    }

    return render(request, 'noticias/editar_noticia.html', context)

# Eliminar una noticia por su ID
@permission_required('noticias.delete_noticia', raise_exception=True)
def eliminar_noticia(request, noticia_id):
    noticia = Noticia.objects.get(noticia_id=noticia_id)

    if request.method == 'POST':
        noticia.delete()
        return redirect("apps.noticias:todas_las_noticias")

    context = {
        "noticia": noticia
    }

    return render(request, 'noticias/eliminar_noticia.html', context)

# Página de inicio ( este es el index.html principal) - 
def inicio(request):
    todas_las_categorias = categorias()
    todas_las_noticias = Noticia.objects.all().order_by('-noticia_id')
    # Noticias para otras secciones
    noticia_principal = Noticia.objects.first()
    noticias_secundarias = Noticia.objects.all()[1:5]
    noticias_destacadas = Noticia.objects.all()[:10]
    ultimas_noticias = Noticia.objects.all()[:8]
    noticias_trending = Noticia.objects.all()[:5]

    # noticias de las últimas 24 horas
    ultima_hora = timezone.now() - timedelta(days=1)
    noticias_ultima_hora = Noticia.objects.filter(fecha__gte=ultima_hora).order_by('-fecha')[:10]

    paginator = Paginator(todas_las_noticias, 8)
    num_pagina = request.GET.get('page')
    pagina_noticia = paginator.get_page(num_pagina)

    context = {
        'pagina_noticia' : pagina_noticia,
        'noticia_principal': noticia_principal,
        'noticias_secundarias': noticias_secundarias,
        'noticias_destacadas': noticias_destacadas,
        'ultimas_noticias': ultimas_noticias,
        'noticias_trending': noticias_trending,
        'noticias_ultima_hora': noticias_ultima_hora,
        'todas_las_categorias' : todas_las_categorias,
    }
    
    return render(request, 'index.html', context)

# Vista Nosotros
def nosotros(request):
    return render(request, 'nosotros.html')

# Vista Contacto
            #def contacto(request):
            # return render(request, 'contact.html')

@login_required
def contacto(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        asunto = request.POST.get('asunto')
        contenido = request.POST.get('contenido')

        # Guardar en la BD
        ContactMessage.objects.create(
            usuario=request.user,
            asunto=asunto,
            contenido=contenido
        )

        # Redirigir a la misma página para evitar reenviar al refrescar
        return JsonResponse({'status': 'success', 'message': 'Mensaje enviado correctamente'})

    return render(request, 'contact.html')

# Noticias en tendencia

def tendencias(request):
    todas_las_categorias = categorias()
    noticias_trending = Noticia.objects.all()[:5]

    context = {
        'todas_las_categorias': todas_las_categorias,
        'noticias_trending' : noticias_trending
    }

    return render(request, 'componentes/tendencias.html', context)


#Visualizar la vista terminos y condiciones
def terminos_condiciones(request):
    return render(request, 'terminos_condiciones.html')

def es_redactor(user):
    return user.groups.filter(name='redactor').exists()

@login_required
@user_passes_test(es_redactor)
def panel_redactor(request):
    # Obtenemos las noticias que creó el usuario q tiene el rol de redactor
    noticias_usuario = Noticia.objects.filter(autor=request.user).order_by('-fecha')

    context = {
        'noticias_usuario': noticias_usuario
    }
    return render(request, 'noticias/panel_redactor.html', context)