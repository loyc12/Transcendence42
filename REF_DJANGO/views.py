# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
# def master(request):
#     return render(request, 'master/master.html')

def login(request):
    template = loader.get_template('login.html')
    # return HttpResponse(template.render())
    return render(template.render())

def select(request):
    template = loader.get_template('select.html')
    return HttpResponse(template.render())
    # return render(request, '.html')

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())
    # return render(request, 'home.html')

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())
