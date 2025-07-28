app_name = 'apps.usuarios'

from django.urls import path

from apps.usuarios.views import login_view, logout_view, register_view

app_name = "apps.usuarios"

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login' ),
    path('logout/', logout_view, name='logout'),
    # path()
]