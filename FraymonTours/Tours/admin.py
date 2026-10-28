from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from django import forms
from Tours.models import Reserva, Viajes, Empleado, Cargo, Departamento, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0
    fields = ('rol',)
    verbose_name = 'Perfil de usuario'
    verbose_name_plural = 'Perfil de usuario'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_rol')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    def get_rol(self, obj):
        try:
            return obj.profile.rol
        except UserProfile.DoesNotExist:
            return 'Sin perfil'
    get_rol.short_description = 'Rol'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


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

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol')
    list_filter = ('rol',)
    search_fields = ('user__username', 'user__email')
    autocomplete_fields = ('user',)

admin.site.register(Cargo)
admin.site.register(Departamento)