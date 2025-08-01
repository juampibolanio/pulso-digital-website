from django.urls import path
from . import views

urlpatterns = [
    path('noticia/<int:noticia_id>/', views.detalle_noticia, name='detalle_noticia'),
]