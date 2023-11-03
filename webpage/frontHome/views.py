from django.http import HttpResponse
from django.template import loader

# from articles.models import Article


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
    

    #     return HttpResponse
    #     return render(request, 'master/master.html')
# def index(request):
#     template = loader.get_template('index.html')
#     # return HttpResponse(template.render())
#     # return render(template.render())
#     return render(template.render())

# Create your views here.
# def master(request):
#     return render(request, 'master/master.html')