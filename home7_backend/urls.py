from django.urls import include, path

urlpatterns = [
    path('api/floorplans/', include('floorplans.urls')),
]
