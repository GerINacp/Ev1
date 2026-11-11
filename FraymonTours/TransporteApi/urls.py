from django.urls import path
from . import views

urlpatterns = [
    path('tours/', views.tours_api, name='api_tours'),
    path('tours/<int:tour_id>/', views.tour_detail_api, name='api_tour_detail'),
    path('external/', views.external_tours_api, name='api_external_tours'),
    path('google-places/', views.google_places_tours_api, name='api_google_places_tours'),
]
