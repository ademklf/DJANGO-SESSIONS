from django.shortcuts import render, HttpResponse, get_object_or_404

from .models import Student, Path

from .serializers import StudentSerializer, PathSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view() #default GET
def home (reguest):
    return Response({'home': 'This is home page...'}) 

# http methods ----------------->
# - GET (DB den veri çağırma, public)
# - POST (DB de değşiklik, create, private)
# - PUT (DB de kayıt değişikliği, private)
# - delete (DB de kayıt silme)
# - patch (kısmi update değişiklik olan yerler güncellenir)

@api_view(['GET'])
def students_list(reguest):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)  # birden çok olduğunda many=True yazılır.
    return Response(serializer.data)

@api_view(['POST'])
def student_create(reguest):
    serializer = StudentSerializer(data=reguest.data)
    if serializer.is_valid():
        serializer.save()
        message ={
            "message":f'Student updated successfully ...'
        }
        return Response(message, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #status kodlar burada belirlenebilir ve kullanıcının doğru bilgilendirilmesi iyi olur.

@api_view(['GET'])
def student_detail(reguest, pk):
    student = get_object_or_404(Student, id=pk)
    serializer = StudentSerializer(student)
    return Response(serializer.data)
 
@api_view(['PUT'])
def student_update(reguest, pk):
    student = get_object_or_404(Student, id=pk)
    serializer = StudentSerializer(student, data=reguest.data)
    if serializer.is_valid():
        serializer.save()
        message ={
            "message":f'Student updated successfully ...'
        }
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def student_delete(reguest,pk):
    student = get_object_or_404(Student, id=pk)
    student.delete()
    message = { 
        "message": 'Student deleted succesfully ...'
    }
    return Response(message)

#############################################################

@api_view(['GET', 'POST'])
def student_api(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Student {serializer.validated_data.get('first_name')} saved successfully!"}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def student_api_get_update_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Student {student.last_name} updated successfully"
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = StudentSerializer(student, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Student {student.last_name} updated successfully"
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        student.delete()
        data = {
            "message": f"Student {student.last_name} deleted successfully"
        }
        return Response(data)