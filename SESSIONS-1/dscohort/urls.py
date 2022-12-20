
from django.urls import path, include
from .views import homeds


urlpatterns = [
   
    path('/', homeds),
   
    
]
