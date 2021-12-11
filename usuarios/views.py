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
            usuario = usuarios.Usuario.objects.get(id=r.usuario_id)
            num_com_por_resp.append([r,len(com),usuario])     
                    
        return render(request,'respuestas.html',{"respuestas":num_com_por_resp,"id_pregunta":request.GET.get("id","")})
    
    elif request.GET.get("confi",""):
        respuestas = list(usuarios.Respuesta.objects.filter(pregunta_id=pregunta.id, confiabilidad_id = 2))       
        num_com_por_resp = []
        for r in respuestas:
            com= list(usuarios.Comentario.objects.filter(respuesta_id=r.id))
            usuario = usuarios.Usuario.objects.get(id=r.usuario_id)
            num_com_por_resp.append([r,len(com),usuario])              
        return render(request,'respuestas.html',{"respuestas":num_com_por_resp})
    
    respuestas = list(usuarios.Respuesta.objects.filter(pregunta_id=pregunta.id,confiabilidad_id = 2))
    num_com_por_resp = []
    for r in respuestas:
        com= list(usuarios.Comentario.objects.filter(respuesta_id=r.id))
        usuario = usuarios.Usuario.objects.get(id=r.usuario_id)
        num_com_por_resp.append([r,len(com),usuario])

    return render(request,'pregunta.html',{"pregunta":pregunta,"respuestas":num_com_por_resp,"temas":temas,"areas":areas,"id_pregunta":request.GET.get("id","")})

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
            return HttpResponse('{"likes":'+str(respuesta.num_buena_calificacion)+',"dislikes":'+str(respuesta.num_mala_calificacion)+'}')

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
            return HttpResponse('{"likes":'+str(respuesta.num_buena_calificacion)+',"dislikes":'+str(respuesta.num_mala_calificacion)+'}')
    
    return HttpResponse('{"likes":'+str(respuesta.num_buena_calificacion)+',"dislikes":'+str(respuesta.num_mala_calificacion)+'}')


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
    indices = ["enunciado__icontains", "area_id", "tema_id", "fecha_de_modificacion__gte"]
    enunciado = request.GET.get("enum","")
    area = request.GET.get("id_ar","")
    tema = request.GET.get("id_tem","")
    fecha = request.GET.get("date","")
    objetos = [enunciado, area, tema, fecha]
    filtro = {}
    
    for i in range (4):
        if objetos[i] != "":
            filtro[indices[i]]=objetos[i]      
    preguntas=list(usuarios.Pregunta.objects.filter(**filtro))
    return render(request,"busqueda.html",{"preguntas":preguntas}) 

def aniadir_respuesta(request):
    usuario=request.GET.get("usuario","")
    pregunta_id=request.GET.get("pregunta_id","")
    contenido=request.GET.get("contenido","")
    ahora = dt.now()
    fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
    usuario=usuarios.Usuario.objects.get(usuario=usuario)
    respuesta_nueva=usuarios.Respuesta(
        contenido=contenido,
        num_buena_calificacion=0,
        num_mala_calificacion=0,
        fecha_de_creacion=fecha,
        fecha_de_modificacion=fecha,
        estado=1,
        confiabilidad_id=1,
        pregunta_id=int(pregunta_id),
        usuario_id=usuario.id                
    )
    respuesta_nueva.save()
    return HttpResponse("se añadio respuesta "+str(usuario)+" "+str(usuario.id))

def eliminar_respuesta(request):
    respuesta_id=request.GET.get("respuesta_id","")
    resp_eliminada=usuarios.Respuesta.objects.get(id=respuesta_id).delete()
    return HttpResponse("se elimino")