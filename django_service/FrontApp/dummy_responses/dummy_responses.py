from django.shortcuts import render


class dummy:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname


# Create your views here.
def dummy_say_hello_to_my_little_puppy(request):
    print(request)
    #return HttpResponse('Hello little puppy !')
    #return render(request, 'hello.html')
    return render(request, 'hello.html', {'name': 'puppy'})

def dummy_say_generic_hello(request):
    print(request)
    #return HttpResponse('Hello little puppy !')
    #return render(request, 'hello.html')
    return render(request, 'hello.html')#, {'name': 'generic person'})

def dummy_list_members(request, context):

    #members = [
    #    dummy('Ginette', 'Légarré'),
    #    dummy('Jonny', 'Rousseau')
    #    #42
    #]
    return (render(request, 'list_components.html', context))