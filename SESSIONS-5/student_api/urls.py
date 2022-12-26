from django.urls import path
from .views import (
    home,
    students_list,
    )

urlpatterns = [
    path("", home),
    path("student-list/", students_list, name = 'list'),
    
]
