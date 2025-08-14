from .models import Categoria

def categorias_globales(request):
    """
    Permite tener las categorias en todos los templates, sin tener que pasarlos por contextos en cada view donde se las necesita
    """

    categorias = Categoria.objects.all()
    print(categorias)
    for cat in categorias:
        print(cat.categoria_id)
    return {
        'categorias_menu': categorias
    }


def es_redactor(request):
    if request.user.is_authenticated:
        es_redactor = request.user.groups.filter(name='redactor').exists()
        return {'es_redactor': es_redactor}
    return {'es_redactor': False}