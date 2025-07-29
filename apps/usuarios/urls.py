app_name = 'apps.usuarios'

from django.urls import path
from apps.usuarios.views import login_view, logout_view, register_view
from django.contrib.auth import views as auth_views

app_name = "apps.usuarios"

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login' ),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path()
]