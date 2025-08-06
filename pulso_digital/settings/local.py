from .base import *
from decouple import config

# Configuración Local

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3308'),
    }
} 

# Configuración del email que enviará el correo a los usuarios para reestablecer la contraseña. El correo y contraseña debe ir luego en el .env
# Mientras estemos en local, el reset de password se puede ver por la consola, cuando vayamos a producción, vamos a usar un correo real 
# para que mande el mensaje al usuario

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # cambiar luego por 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#EMAIL_HOST_USER = 'correo-de-gmail@gmail.com'
#EMAIL_HOST_PASSWORD = 'contrasenia-de-gmail'