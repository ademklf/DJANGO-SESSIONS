from .pagination import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, HttpResponse, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, mixins, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import(
     IsAuthenticated,
     IsAdminUser,
     IsAuthenticatedOrReadOnly,
)


from .models import Student, Path
from .serializers import StudentSerializer, PathSerializer


#!######################## FUNCTİON BASED VİEWS ####################################

@api_view() #default GET
def home (reguest):
    return Response({'home': 'This is home page...'}) 

# http methods ----------------->
# - GET (DB den veri çağırma, public)# - POST (DB de değşiklik, create, private)
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


######################### CLASS BASED VİEWS ####################################

#! API VİEW
class StudentListCreate(APIView):
    
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Student {serializer.validated_data.get('first_name')} saved successfully!"}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StudentDetail(APIView):
    
    def get_obj(self, pk):
        return get_object_or_404(Student, pk=pk)
    
    def get(self, request, pk):
        student = self.get_obj(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    def put(self, request, pk):
        student = self.get_obj(pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Student {student.last_name} updated successfully"
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        student = self.get_obj(pk)
        student.delete()
        data = {
            "message": f"Student {student.last_name} deleted successfully"
        }
        return Response(data)


#!GENERİC VİEWS
''' #? GenericApıView
# One of the key benefits of class-based views is the way they allow you to compose bits of reusable behavior. REST framework takes advantage of this by providing a number of pre-built views that provide for commonly used patterns.

# GenericAPIView class extends REST framework's APIView class, adding commonly required behavior for standard list and detail views.

#? Mixins
# - ListModelMixin
#     - list method
# - CreateModelMixin
#     - create method
# - RetrieveModelMixin
#     - retrieve method
# - UpdateModelMixin
#     - update method
# - DestroyModelMixin
#     - destroy method '''

class StudentGAV(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class StudentDetailGAV(mixins.RetrieveModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    queryset = Student.objects.all()
    serializer_class= StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#! Concrete Views


class StudentCV(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetailCV(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

#! ViewSets


# - Django REST framework allows you to combine the logic for a set of related views in a single class, called a ViewSet. 

# - Typically, rather than explicitly registering the views in a viewset in the urlconf, you'll register the viewset with a router class, that automatically determines the urlconf for you.

# There are two main advantages of using a ViewSet class over using a View class.

#  - Repeated logic can be combined into a single class. In the above example, we only need to specify the queryset once, and it'll be used across multiple views.
#  - By using routers, we no longer need to deal with wiring up the URL conf ourselves.

# Both of these come with a trade-off. Using regular views and URL confs is more explicit and gives you more control. ViewSets are helpful if you want to get up and running quickly, or when you have a large API and you want to enforce a consistent URL configuration throughout.



class StudentMVS(ModelViewSet):
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination
    # pagination_class = CustomLimitOffsetPagination
    # pagination_class = CustomCursorPagination
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields= ['id', 'first_name','last_name']
    search_fields = ['first_name','last_name']
    
    
    


    @action(detail=False, methods=["GET"])
    def student_count(self, request):
        count = {
            "student-count" : self.queryset.count()
        }
        return Response(count)
    
    
class PathMVS(ModelViewSet):

    queryset = Path.objects.all()
    serializer_class = PathSerializer
    
    @action(detail=True)
    def student_names(self, request, pk=None):
        path = self.get_object()
        students = path.students.all()
        return Response([i.first_name for i in students])