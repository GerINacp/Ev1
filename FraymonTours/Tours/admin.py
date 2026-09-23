# Register your models here.
from django.contrib import admin

# Register your models here.
from Tours.models import Reserva, Viajes, Empleado


class CargoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_cliente']


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre']


class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['run', 'nombre', 'paterno', 'materno',
                    'codigoEmpleado', 'sueldo',
                    'fechaNac', 'cargo', 'departamento']


admin.site.register(Reserva, CargoAdmin)
admin.site.register(Viajes, DepartamentoAdmin)
admin.site.register(Empleado, EmpleadoAdmin)

