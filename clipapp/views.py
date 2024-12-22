from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'clipapp/index.html')

def home(request):
    return render(request, 'clipapp/home.html')


def login_view(request):
    return render(request, 'clipapp/login.html')