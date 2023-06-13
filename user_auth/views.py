from django.shortcuts import render
from django.http import HttpResponse


from . import views

def test(request):
    return HttpResponse("This is the authentication app")