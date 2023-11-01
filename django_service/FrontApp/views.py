from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def start(request):
    return render(request, 'home/init.html')

def login(request):
    return render(request, 'home/select.html')

def home(request):
    return render(request, 'home/home.html')
