from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home (reguest):
    return HttpResponse('This is our home page ....')