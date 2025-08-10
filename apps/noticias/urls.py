app_name = 'apps.noticias'

from django.urls import path
from .views import (
    noticias,
    detalle_noticia,
    crear_noticia,
    editar_noticia,
    eliminar_noticia,
    categoria, 
    nosotros,   
    contacto,    
    terminos_condiciones
)

urlpatterns = [
    path('', noticias, name="todas_las_noticias"), # Muestra todas las noticias
    
    path('categorias/', categorias, name='categorias'),  # ruta para categorías

    path('categoria/<int:categoria_id>/', categoria, name='categoria_por_id'), # Ruta para noticias x categoria
    
    path('nosotros/', nosotros, name='nosotros'), # Ruta para template Nosotros

    path('contact/', contacto, name='contacto'), # Ruta para template contacto
    
    path('<int:noticia_id>/', detalle_noticia, name="detalle_noticia"), # Muestra la noticia al detalle

    path('crear/', crear_noticia, name="crear_noticia"), # Crear una noticia

    path('editar/<int:noticia_id>/', editar_noticia, name ="editar_noticia"), # Editar una noticia
    
    path('eliminar/<int:noticia_id>/', eliminar_noticia, name ="eliminar_noticia"), #Eliminar una noticia

    path('terminos/', terminos_condiciones, name='terminos_condiciones'),
    
]