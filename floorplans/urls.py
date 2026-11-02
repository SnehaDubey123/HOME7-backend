from django.urls import path
from .views import generate_floorplan

urlpatterns = [
    path('generate/', generate_floorplan, name='generate-floorplan'),
]
