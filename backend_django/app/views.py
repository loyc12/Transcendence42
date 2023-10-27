from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def say_hello_to_my_little_puppy(request):
    print(request)
    #return HttpResponse('Hello little puppy !')
    #return render(request, 'hello.html')
    return render(request, 'hello.html', {'name': 'bobby'})

