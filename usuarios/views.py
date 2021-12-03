from django.shortcuts import render
from django.http import HttpResponse
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
    pregunta = usuarios.Pregunta.objects.get(id=request.GET.get('id',''))
    respuestas = list(usuarios.Respuesta.objects.filter(pregunta_id=pregunta.id))
    return render(request,'pregunta.html',{"pregunta":pregunta,"respuestas":respuestas})