from django.http import HttpResponse
from django.shortcuts import render, redirect
#Clases importadas para el login
from django.contrib import messages
from validate_email import validate_email
from usuarios import models as usuarios
from datetime import datetime as dt
#from .models import usuarios

def hola(request):
    return HttpResponse("Hola mundo")

# Funciones de Internacionalizacion
def index(request):
    return render(request, "index.html",{})

#Nuevo Registro 
def register(request):
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        #Validacion de la longitud de la contrasenia
        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 
            'El tamaño de la contraseña debe ser mayor a 6 caracteres')
            context['has_error'] = True
        #Validacion de las contrasenias iguales
        if password != password2:
            messages.add_message(request, messages.ERROR, 
            'Las contraseñas no coinciden')
            context['has_error'] = True
        #Validacion del correo electronico
        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 
            'Ingrese un correo electrónico válido')
            context['has_error'] = True
        if not username:
            messages.add_message(request, messages.ERROR, 
            'El nombre de usuario es requerido')
            context['has_error'] = True
        #Validaciones si ya existe el nombre de usuario o 
        #el correo electronico
        if usuarios.Usuario.objects.filter(usuario=username).exists():
            messages.add_message(request, messages.ERROR, 
            'El nombre de usuario ya existe')
            context['has_error'] = True
        if usuarios.Usuario.objects.filter(correo=email).exists():
            messages.add_message(request, messages.ERROR, 
            'El correo electrónico ya existe')
            context['has_error'] = True

        #Si existe algun error se redirecciona nuevamente al registro
        if context['has_error']:
            return render(request, 'register.html', context)

        #Se obtiene la fecha y hora actual
        ahora = dt.now()
        fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")

        user = usuarios.Usuario(
                usuario = username,
                correo = email,
                contrasenia = password,
                fecha_de_creacion = fecha,
                fecha_de_modificacion = fecha,
                #faltaria el nivel
                estado=True)
        user.save()
        messages.add_message(request, messages.SUCCESS, 
            'La cuenta ha sido creada, ya puede iniciar sesion')
        return redirect('login')
    return render(request, 'register.html')

#Nuevo Login
def login(request):
    return render(request, 'login.html')