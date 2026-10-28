from django.contrib import admin
from Tours.models import Reserva, Viajes, Empleado

# Registro directo sin clases de personalización avanzadas para evitar el fallo de Python 3.15
admin.site.register(Reserva)
admin.site.register(Viajes)
admin.site.register(Empleado)