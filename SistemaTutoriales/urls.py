"""SistemaTutoriales URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
#clases propias

from SistemaTutoriales.views import index
from usuarios import views as vu

#Para el login que trae Django
from django.contrib.auth.views import LoginView, LogoutView
#Para indicar que es necesario loguearse
from django.contrib.auth.decorators import login_required

#from SistemaTutoriales/views.py import hola
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    #url(r'^foro/$', vu.foro),
    url(r'^pregunta/$',vu.pregunta),
    url(r'^comentario/$',vu.comentario),
    url(r'^calificacion/$',vu.calificacion),
    path('foro/', vu.foro, name='foro'),
    #ruta para el registro, login y logout
    path('registro/', vu.registro, name='registro'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    #ruta del search
    path('search_e/', vu.search_e),
]