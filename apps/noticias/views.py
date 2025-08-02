from django.shortcuts import get_object_or_404, render

from apps.comentarios.forms import ComentarioForm
from apps.comentarios.models import Comentario
from .models import Categoria, ImagenNoticia, Noticia
from .forms import NoticiaForm
from django.shortcuts import redirect

#Listar todas las noticias
def noticias(request):
    noticias = Noticia.objects.all()
    categorias = Categoria.objects.all()

    params = request.GET.get('categoria', '').strip()

    if params:
        noticias = noticias.filter(categorias__nombre__icontains=params)

    context = {
        "noticias": noticias,
        "categorias": categorias
    }   

    return render(request, 'noticias/noticias.html', context)

#Noticia Detalle

def detalle_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    comentarios = Comentario.objects.filter(noticia=noticia).order_by('-fecha')
    imagenes = noticia.imagenes.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                nuevo_comentario = form.save(commit=False)
                nuevo_comentario.user = request.user
                nuevo_comentario.noticia = noticia
                nuevo_comentario.save()
                return redirect('apps.noticias:detalle_noticia', noticia_id=noticia_id)
        else:
            return redirect('login')
    else:
        form = ComentarioForm()

    return render(request, 'noticias/detalle_noticia.html', {
        'detalle': noticia,
        'comentarios': comentarios,
        'form': form,
        'imagen': imagenes  
    })



#Crear noticia
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
        form = NoticiaForm()

    context = {
        "form": form
    }

    return render(request, 'noticias/crear_noticia.html', context)


#Editar una noticia por su ID
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



#Eliminar una noticia por su ID
def eliminar_noticia(request, noticia_id):
    noticia = Noticia.objects.get(noticia_id=noticia_id)

    if request.method == 'POST':
        noticia.delete()
        return redirect("apps.noticias:todas_las_noticias")

    context = {
        "noticia": noticia
    }

    return render(request, 'noticias/eliminar_noticia.html', context)

# CREO LA VISTA CATEGORIA 

def categoria(request):
    return render(request, 'category.html')

# Página de inicio (index.html principal) -
def inicio(request):
    # obtenemos las noticias más recientes para diferentes secciones de la pagina
    noticia_principal = Noticia.objects.first()  # La noticia más reciente la pongo en el slider principal (la seccion de arriba del todo)
    noticias_secundarias = Noticia.objects.all()[1:5]  # Las siguientes 4 noticias para las tarjetas mas chicas
    noticias_destacadas = Noticia.objects.all()[:2]  # 2 noticias para la sección destacadas
    ultimas_noticias = Noticia.objects.all()[:8]  # 8 noticias para la sección de últimas noticias
    noticias_trending = Noticia.objects.all()[:5]  # 5 noticias para trending en el sidebar
    # coloque  [:número] para que me traiga una cantidad determinada de noticias.
    
    context = {
        'noticia_principal': noticia_principal,
        'noticias_secundarias': noticias_secundarias,
        'noticias_destacadas': noticias_destacadas,
        'ultimas_noticias': ultimas_noticias,
        'noticias_trending': noticias_trending,
    }
    
    return render(request, 'index.html', context)

#CREO LA VISTA NOSOTROS
def nosotros(request):
    return render(request, 'nosotros.html')

def contacto(request):
    return render(request, 'contact.html')