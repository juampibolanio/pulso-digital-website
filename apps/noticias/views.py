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
    noticia = Noticia.objects.get(noticia_id)

    context = {
        "detalle": noticia
    }

    return render(request, 'noticias/detalle_noticia.html', context)

#Crear noticia
def crear_noticia(request):
    
    if request.method =='POST':
        form = NoticiaForm(request.POST)
        imagenes = request.FILES.getlist('imagen')


        if form.is_valid():
            form.save()

            for imagen in imagenes:
                ImagenNoticia.objects.create(form=form, imagen=imagen)

            return redirect("todos_las_noticias")
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
        if form.is_valid():
            form.save()
            return redirect("detalle_noticia", noticia_id=noticia.noticia.id)
    else:
        form = NoticiaForm(instante=noticia)

    context = {
        "form": form
    }

    return render(request, 'noticias/editar_noticia.html', context)    

#Eliminar una noticia por su ID
def eliminar_noticia(request, noticia_id):
    noticia = Noticia.objects.get(noticia_id=noticia_id)

    if request.method == 'POST':
        noticia.delete()
        return redirect("todas_las_noticias")

    context = {
        "noticia": noticia
    }

    return render(request, 'noticias/eliminar_noticia.html', context)
