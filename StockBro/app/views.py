from django.shortcuts import render

from django.shortcuts import HttpResponse
# Create your views here.


def home(request):

    return HttpResponse("<h1> Welcome to my page</h1>")
