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
    temas = list(usuarios.Tema.objects.all())
    areas = list(usuarios.Area.objects.all())
    return render(request,'foro.html',{"preguntas": preguntas,"temas":temas,"areas":areas})

def pregunta(request):
    #recibimos el id de la pregunta seleccionada en foro
    temas = list(usuarios.Tema.objects.all())
    areas = list(usuarios.Area.objects.all())
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
        
        num_com_por_resp = []
        for r in respuestas:
            '''
            com_resp= list(usuarios.Comentario.objects.filter(respuesta_id=r.id, comentario_id= null))
            num_com_resp = len(com_resp)
            '''
            com= list(usuarios.Comentario.objects.filter(respuesta_id=r.id))
            num_com_por_resp.append([r,len(com)])     
                    
        return render(request,'respuestas.html',{"respuestas":num_com_por_resp})
    
    elif request.GET.get("confi",""):
        respuestas = list(usuarios.Respuesta.objects.filter(pregunta_id=pregunta.id, confiabilidad_id = 2))       
        num_com_por_resp = []
        for r in respuestas:
            com= list(usuarios.Comentario.objects.filter(respuesta_id=r.id))
            num_com_por_resp.append([r,len(com)])                  
        return render(request,'respuestas.html',{"respuestas":num_com_por_resp})
    
    respuestas = list(usuarios.Respuesta.objects.filter(pregunta_id=pregunta.id,confiabilidad_id = 2))
    num_com_por_resp = []
    for r in respuestas:
        com= list(usuarios.Comentario.objects.filter(respuesta_id=r.id))
        num_com_por_resp.append([r,len(com)]) 

    return render(request,'pregunta.html',{"pregunta":pregunta,"respuestas":num_com_por_resp,"temas":temas,"areas":areas})

def comentario(request):
    respuesta_id=request.GET.get("id_respuesta","")
    comentario_id=request.GET.get("id_comentario","")
    comentarios=[]
    if (not comentario_id):
        comentarios=list(usuarios.Comentario.objects.filter(respuesta_id = respuesta_id, comentario_id__isnull = True))
    else:
        comentarios=list(usuarios.Comentario.objects.filter(comentario_id = comentario_id))
    
    num_scom_com=[]

    for comentario in comentarios:
        com= list(usuarios.Comentario.objects.filter(comentario_id=comentario.id))
        num_scom_com.append([comentario,len(com)])
    return render(request,'comentario.html',{"comentarios":num_scom_com})

#likes y dislikes
def calificacion(request):
    usuario=request.GET.get("usuario","")
    usuario=usuarios.Usuario.objects.get(usuario=usuario)
    cal=request.GET["like"] if request.GET.get("like","") else request.GET["dislike"]
    respuesta=usuarios.Respuesta.objects.get(id=cal)
    if request.GET.get("like",""):
        if usuarios.Calificacion.objects.filter(usuario_id=usuario.id,respuesta_id=cal).exists():
            
            califi=list(usuarios.Calificacion.objects.filter(usuario_id=usuario.id,respuesta_id=cal))[0]
            print(califi.estado)
            if (califi.estado == True):
                respuesta.num_buena_calificacion=respuesta.num_buena_calificacion-1
                respuesta.save()
                califi.delete()
            else:
                califi.estado = True
                respuesta.num_buena_calificacion=respuesta.num_buena_calificacion+1
                respuesta.num_mala_calificacion=respuesta.num_mala_calificacion-1
                respuesta.save()
                califi.save()
        
        else:
            ahora = dt.now()
            fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
            califi=usuarios.Calificacion(
                fecha_de_creacion=fecha,
                fecha_de_modificacion=fecha,
                estado=True,
                respuesta_id=cal,
                usuario_id=usuario.id                
            )
            califi.save()
            respuesta.num_buena_calificacion=respuesta.num_buena_calificacion+1
            respuesta.save()
            return HttpResponse(respuesta.num_buena_calificacion)

    elif request.GET.get("dislike",""):
        if usuarios.Calificacion.objects.filter(usuario_id=usuario.id,respuesta_id=cal).exists():
            
            califi=list(usuarios.Calificacion.objects.filter(usuario_id=usuario.id,respuesta_id=cal))[0]
            print(califi.estado)
            if (califi.estado == False):
                respuesta.num_mala_calificacion=respuesta.num_mala_calificacion-1
                respuesta.save()
                califi.delete()
            else:
                califi.estado = False
                respuesta.num_buena_calificacion=respuesta.num_buena_calificacion-1
                respuesta.num_mala_calificacion=respuesta.num_mala_calificacion+1
                respuesta.save()
                califi.save()
        
        else:
            ahora = dt.now()
            fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
            califi=usuarios.Calificacion(
                fecha_de_creacion=fecha,
                fecha_de_modificacion=fecha,
                estado=False,
                respuesta_id=cal,
                usuario_id=usuario.id                
            )
            califi.save()
            respuesta.num_mala_calificacion=respuesta.num_mala_calificacion+1
            respuesta.save()
            return HttpResponse(respuesta.num_mala_calificacion)
    
    return HttpResponse("0")

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
#buscar
def search_e(request):
   
    preguntas=[]
    if (request.GET.get("enum","")):
        enuncia=request.GET["enum"]
        preguntas=list(usuarios.Pregunta.objects.filter(enunciado__icontains=enuncia))
    
    if (request.GET.get("id_ar","")):
        id_area=request.GET["id_ar"]
        if not len(preguntas) :
            preguntas=list(usuarios.Pregunta.objects.filter(area_id=id_area))
        else:
            for pregunta in preguntas:
                if int(pregunta.area_id)==int(id_area):
                    preguntas.append(pregunta)

    if (request.GET.get("id_tem","")) :
        id_tema=request.GET["id_tem"]
        if not len(preguntas) :
            preguntas=list(usuarios.Pregunta.objects.filter(tema_id=id_tema))
        else:
            ptemp=preguntas
            preguntas=[]
            for pregunta in ptemp:
                if int(pregunta.tema_id)==int(id_tema):
                    preguntas.append(pregunta)
    '''
    arrraylist=()
    arraylist2=()
    if request.GET["enun"]
        arraylist.add(enun)
        arraylis2.add(enunciado__icontains)
    if request.GET["id_ar"]
        arraylis2.add(area_id)
        arraylist.add(id_ar)
    if request.GET["id_tem"]
        arraylist.add(id_team)
        arraylis2.add(tema_id)
    if request.GET["date"]
        arraylist.add()
        arraylis2.add(fecha_de_modificacion)
    for arraylist 
       pregunta=list(usuarios.Pregunta.objects.filter(array(0)=arraylist(0))) 
       
    '''
    if (request.GET.get("date","")) :
        dt=request.GET["date"]
        if not len(preguntas) :
            preguntas=list(usuarios.Pregunta.objects.filter(fecha_de_modificacion=dt))
        else:
            ptemp=preguntas
            preguntas=()
            for pregunta in ptemp:
                if pregunta.fecha_de_modificacion==dt:
                    preguntas.append(pregunta)
    if not len(preguntas):
        preguntas=[]
    return render(request,"busqueda.html",{"preguntas":preguntas})       
