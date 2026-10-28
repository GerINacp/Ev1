from django.contrib import admin
from django.db import models
from django import forms
from Tours.models import Reserva, Viajes, Empleado, Cargo, Departamento

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('nombre_cliente', 'tour', 'fecha_reserva', 'cantidad_personas')

@admin.register(Viajes)
class ViajesAdmin(admin.ModelAdmin):
    # CORREGIDO: Usamos 'codigo', 'nombre' (en vez de 'titulo') y eliminamos 'precio' si no existe
    list_display = ('codigo', 'nombre', 'creado')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    # CORREGIDO: Usamos 'paterno' y 'materno' tal como los tienes en models.py
    list_display = ('run', 'nombre', 'paterno', 'materno', 'cargo', 'departamento')
    
    # Esto mantiene el calendario moderno para la fecha de nacimiento
    formfield_overrides = {
        models.DateField: {'widget': forms.DateInput(attrs={'type': 'date'})},
    }

# Opcional: Registra también Cargo y Departamento para poder crearlos desde el admin
admin.site.register(Cargo)
admin.site.register(Departamento)