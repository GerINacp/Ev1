from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from django import forms
from Tours.models import Reserva, Viajes, Empleado, Cargo, Departamento, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol')
    list_filter = ('rol',)
    search_fields = ('user__username', 'user__email')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('nombre_cliente', 'tour', 'fecha_reserva', 'cantidad_personas', 'estado')

@admin.register(Viajes)
class ViajesAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'precio', 'creado')
    list_editable = ('precio',)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('run', 'nombre', 'paterno', 'materno', 'cargo', 'departamento')
    formfield_overrides = {
        models.DateField: {'widget': forms.DateInput(attrs={'type': 'date'})},
    }



admin.site.register(Cargo)
admin.site.register(Departamento)