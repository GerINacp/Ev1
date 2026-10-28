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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)