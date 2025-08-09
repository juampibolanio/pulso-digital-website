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
        form = NoticiaForm(instance=noticia)

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

# CREO LA VISTA CATEGORIA 

def categoria(request):
    return render(request, 'category.html')

# Página de inicio ( este es el index.html principal) - 
def inicio(request):
    todas_las_categorias = categorias()
    # Noticias para otras secciones
    noticia_principal = Noticia.objects.first()
    noticias_secundarias = Noticia.objects.all()[1:5]
    noticias_destacadas = Noticia.objects.all()[:2]
    ultimas_noticias = Noticia.objects.all()[:8]
    noticias_trending = Noticia.objects.all()[:5]

    # noticias de las últimas 24 horas
    ultima_hora = timezone.now() - timedelta(days=1)
    noticias_ultima_hora = Noticia.objects.filter(fecha__gte=ultima_hora).order_by('-fecha')[:10]

    context = {
        'noticia_principal': noticia_principal,
        'noticias_secundarias': noticias_secundarias,
        'noticias_destacadas': noticias_destacadas,
        'ultimas_noticias': ultimas_noticias,
        'noticias_trending': noticias_trending,
        'noticias_ultima_hora': noticias_ultima_hora,
        'todas_las_categorias' : todas_las_categorias
    }
    
    return render(request, 'index.html', context)

#CREO LA VISTA NOSOTROS
def nosotros(request):
    return render(request, 'nosotros.html')

#CREO LA VISTA CONTACTO
def contacto(request):
    return render(request, 'contact.html')

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