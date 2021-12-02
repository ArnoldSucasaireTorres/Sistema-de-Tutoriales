from django.http import HttpResponse
from django.shortcuts import render

def hola(request):
    return HttpResponse("Hola mundo")

# Funciones de Internacionalizacion
def index(request):
    return render(request, "index.html",{})