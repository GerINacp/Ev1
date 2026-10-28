from django.db import models
from django.utils import timezone

class Reserva(models.Model):
    TOURS_CHOICES = [
        ('vina_del_mar', 'Viña del Mar'),
        ('city_tour', 'City Tour'),
        ('farellones', 'Farellones'),
        ('valle_nevado', 'Valle Nevado'),
    ]

    nombre_cliente = models.CharField(max_length=100, verbose_name="Nombre del cliente")
    email = models.EmailField(verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    tour = models.CharField(max_length=50, choices=TOURS_CHOICES, verbose_name="Tour")
    fecha_reserva = models.DateField(verbose_name="Fecha del tour")
    cantidad_personas = models.PositiveIntegerField(default=1, verbose_name="Cantidad de personas")
    creado_el = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        return f"{self.nombre_cliente} - {self.get_tour_display()} ({self.fecha_reserva})"


class Viajes(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Viaje')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    imagen = models.ImageField(upload_to='tours/', blank=True, null=True, verbose_name='Imagen del Tour')
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Viajes'
        verbose_name = 'Viaje'
        verbose_name_plural = 'Tours'


# 1. Agrega estos nuevos modelos arriba o antes de la clase Empleado
class Cargo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Cargo")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"


class Departamento(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Departamento")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"


# 2. Modifica tu clase Empleado existente para que luzca así:
class Empleado(models.Model):
    run = models.CharField(max_length=10, verbose_name='RUN')
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    paterno = models.CharField(max_length=50, verbose_name='Apellido Paterno')
    materno = models.CharField(max_length=50, verbose_name='Apellido Materno')
    codigoEmpleado = models.CharField(max_length=20, verbose_name='Código de Empleado')
    sueldo = models.PositiveIntegerField(default=450000, verbose_name='Sueldo Base')
    fechaNac = models.DateField(null=True, blank=True, verbose_name='Fecha de Nacimiento')
    
    # ¡AQUÍ ESTÁ EL CAMBIO CLAVE! Ahora apuntan a sus modelos correctos en lugar de a 'Viajes'
    cargo = models.ForeignKey(Cargo, null=False, on_delete=models.RESTRICT, related_name='empleados_cargo')
    departamento = models.ForeignKey(Departamento, null=True, on_delete=models.CASCADE, related_name='empleados_departamento')
    
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} {} {}".format(self.nombre, self.paterno, self.materno)

    class Meta:
        db_table = 'empleado'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['nombre', 'paterno', 'materno']