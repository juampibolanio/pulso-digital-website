from django.shortcuts import render
from .models import Noticia, Categoria, ImagenNoticia
from .forms import NoticiaForm, NoticiaImagenForm
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
    noticia = Noticia.objects.get(noticia_id=noticia_id)
    imagenes = ImagenNoticia.objects.filter(noticia_id=noticia_id)

    context = {
        "detalle": noticia,
        "imagen": imagenes
    }

    return render(request, 'noticias/detalle_noticia.html', context)

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
