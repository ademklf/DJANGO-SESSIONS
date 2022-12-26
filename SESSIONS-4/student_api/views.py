
from django.http import HttpResponse

# Create your views here.
def home(reguest):
    return HttpResponse('<h1>API Page</h1>')
