from .models import Categoria

def categorias_globales(request):
    """
    Context processor para hacer las categorías disponibles en todos los templates
    """

    categorias = Categoria.objects.all()
    print(categorias)
    for cat in categorias:
        print(cat.categoria_id)
    return {
        'categorias_menu': categorias
    }