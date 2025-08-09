from django.urls import path
from . import views

urlpatterns = [
    path('<int:noticia_id>/', views.detalle_noticia, name='comentario_por_noticia'),
    path('editar/<int:comentario_id>/', views.editar_comentario, name='editar_comentario'),
    path('eliminar/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
]