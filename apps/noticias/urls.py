app_name = 'apps.noticias'

from django.urls import path
from .views import (
    noticias,
    detalle_noticia,
    crear_noticia,
    editar_noticia,
    eliminar_noticia,
    categoria,  # <-- importá la vista categoria
    nosotros,   # <-- importá la vista nosotros
    contacto    # <-- importá la vista nosotros
)

urlpatterns = [
    path('', noticias, name="todas_las_noticias"), #Muestra todas las noticias
    
    path('categoria/', categoria, name='categoria'),  # <-- ruta para categorías
    
    path('nosotros/', nosotros, name='nosotros'),

    path('contact/', contacto, name='contacto'),
    
    path('<int:noticia_id>/', detalle_noticia, name="detalle_noticia"), #Muestra la noticia al detalle

    path('crear/', crear_noticia, name="crear_noticia"), #Crear una noticia

    path('editar/<int:noticia_id>/', editar_noticia, name ="editar_noticia"), #Editar una noticia
    
    path('eliminar/<int:noticia_id>/', eliminar_noticia, name ="eliminar_noticia"), #Eliminar una noticia
]