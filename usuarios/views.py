from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
#Formularios para en registro en django
from datetime import datetime as dt
from django.contrib import messages
from .forms import UserRegisterForm


# Create your views here.

from usuarios import models as usuarios
import datetime
def foro(request):
    preguntas = list(usuarios.Pregunta.objects.all())
    #fc=datetime.datetime(2021,12,3,10,00)
    #fm=datetime.datetime(2021,12,3,10,00)
    #area2=usuarios.Area(
     #   nombre="Algebra",
      #  fecha_de_creacion=str(fc),
       # fecha_de_modificacion=str(fm),
        #estado=True)
    #area2.save()
    return render(request,'foro.html',{"preguntas": preguntas})

def pregunta(request):
    #recibimos el id de la pregunta seleccionada en foro
    if request.GET.get("id",""):
        try:
            pregunta = usuarios.Pregunta.objects.get(id=request.GET.get('id',''))
            respuestas=()
        except ObjectDoesNotExist:
            return HttpResponse("Pregunta no encontrada")
    else:
        return HttpResponse("pregunta no encontrada")
    #verificamos que las respuestas a la pregunta sea confiable o no
    if request.GET.get("comun",""):
        respuestas = list(usuarios.Respuesta.objects.filter(pregunta_id=pregunta.id, confiabilidad_id = 1))
        return render(request,'respuestas.html',{"respuestas":respuestas})
    elif request.GET.get("confi",""):
        respuestas = list(usuarios.Respuesta.objects.filter(pregunta_id=pregunta.id, confiabilidad_id = 2))
        return render(request,'respuestas.html',{"respuestas":respuestas})
    respuestas = list(usuarios.Respuesta.objects.filter(pregunta_id=pregunta.id,confiabilidad_id = 2))
    return render(request,'pregunta.html',{"pregunta":pregunta,"respuestas":respuestas})

def registro(request):
    #Hacemos un if para verificar si los campos fueron llenados
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #Adeemas de guardar en el Auth User de Django, se
            # guarda tambien en Usuarios_usuario
            nombre_usuario = form.cleaned_data['username']
            email_usuario = form.cleaned_data['email']
            nombre_apellidos_usuario = form.cleaned_data['first_name'] +" "+ form.cleaned_data['last_name']
            contrasenia_usuario = form.cleaned_data['password1']
            #Se obtiene la fecha y hora actual
            ahora = dt.now()
            fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")

            usuario_en_creacion = usuarios.Usuario(
                nombre = nombre_apellidos_usuario,
                usuario = nombre_usuario,
                correo = email_usuario,
                contrasenia = contrasenia_usuario,
                fecha_de_creacion = fecha,
                fecha_de_modificacion = fecha,
                estado=True)
            usuario_en_creacion.save()
            #messages.success(request, f'Usuario {nombre_apellidos_usuario} creado')
            #messages.success(request, f'Usuario {username} creado')
            return redirect('foro')
    else:
        form = UserRegisterForm()
    context = { 'form' : form}
    return render(request, 'registro.html', context)
