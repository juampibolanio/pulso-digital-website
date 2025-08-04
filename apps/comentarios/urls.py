from django.urls import path
from . import views

urlpatterns = [
    path('<int:noticia_id>/', views.detalle_noticia, name='comentario_por_noticia'),
]