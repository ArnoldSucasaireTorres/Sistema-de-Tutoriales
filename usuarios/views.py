from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
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

