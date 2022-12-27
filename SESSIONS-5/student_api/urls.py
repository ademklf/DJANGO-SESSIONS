from django.urls import path
from .views import (
    home,
    students_list,
    student_create,
    student_detail,
    student_update,
    student_delete
    )

urlpatterns = [
    path("", home),
    path("student-list/", students_list, name = 'list'),
    path("student-create/", student_create, name = 'create'),
    path("student-detail/<int:pk>/", student_detail, name = 'detail'),
    path("student-update/<int:pk>/", student_update, name = 'update'),
    path("student-delete/<int:pk>/", student_delete, name = 'delete'),
    
]
