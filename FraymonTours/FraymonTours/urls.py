from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from Tours import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_view, name='landing'),
    path('inicio/', views.legacy_index_redirect, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('cotizar/', views.cotizar_view, name='cotizar'),
    path('empleado/', views.empleado_dashboard, name='empleado_dashboard'),
    path('empleado/perfil/', views.empleado_perfil, name='empleado_perfil'),
    path('empleado/reserva/<int:reserva_id>/estado/', views.cambiar_estado_reserva, name='cambiar_estado_reserva'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/tours/', views.admin_tours, name='admin_tours'),
    path('admin-panel/tours/<int:tour_id>/editar/', views.admin_editar_tour, name='admin_editar_tour'),
    path('admin-panel/reserva/<int:reserva_id>/editar/', views.admin_editar_reserva, name='admin_editar_reserva'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)