from django.shortcuts import render, HttpResponse

# Create your views here.

def auth_main(request):
    return HttpResponse('Reached main auth endpoint')

def auth_signin(request):
    return HttpResponse('Reached signin endpoint')


def auth_signup(request):
    return HttpResponse('Reached signup endpoint')


def auth_signout(request):
    return HttpResponse('Reached signout endpoint')
