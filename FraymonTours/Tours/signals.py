from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance, defaults={'rol': 'Cliente'})
    else:
        # Nos aseguramos de buscar o crear el perfil de manera segura sin depender del atributo directo
        UserProfile.objects.get_or_create(user=instance, defaults={'rol': 'Cliente'})