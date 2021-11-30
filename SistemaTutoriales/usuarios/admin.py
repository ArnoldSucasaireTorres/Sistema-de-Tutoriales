from django.contrib import admin

# Register your models here.
from usuarios.models import Usuario

admin.site.register(Usuario)