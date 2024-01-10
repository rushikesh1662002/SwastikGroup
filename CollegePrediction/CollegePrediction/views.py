# views.py
from django.http import HttpResponse
from django.template import loader

def login_view(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def signup_view(request):
    template = loader.get_template('signup.html')
    return HttpResponse(template.render())

def home_view(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
