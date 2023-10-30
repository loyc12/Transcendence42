from django.shortcuts import render
from django.http import HttpResponse
from FrontApp.dummy_responses import dummy_responses as dummy
# import . from dummy_responses.dummy_responses

# Create your views here.
def say_hello_to_my_little_puppy(request):
    print(request)
    return (dummy.dummy_say_hello_to_my_little_puppy(request))
    #return HttpResponse('Hello little puppy !')
    #return render(request, 'hello.html')
    #return render(request, 'hello.html', {'name': 'puppy'})

def say_generic_hello(request):
    print(request)
    return (dummy.dummy_say_generic_hello(request))
    #return HttpResponse('Hello little puppy !')
    #return render(request, 'hello.html')
    #return render(request, 'hello.html')#, {'name': 'generic person'})

def list_members(request):
    members = [
        dummy.dummy('Ginette', 'Légaré'),
        dummy.dummy('Jonny', 'Rousseau')
        #42
    ]
    return (dummy.dummy_list_members(request, {'mymembers': members}))
