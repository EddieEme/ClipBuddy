from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Snippet
from .serializers import SnippetSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie

def index(request):
    return render(request, 'clipapp/index.html')

def home(request):
    return render(request, 'clipapp/home.html')

def register_view(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        
        User = get_user_model()
        
        if password != password1:
            messages.error(request, "Passwords do not match.")
            return render(request, 'clipapp/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "clipapp/register.html")
        
        names = full_name.split(' ')
        first_name = names[0]
        last_name = ' '.join(names[1:]) if len(names) > 1 else ''
        
        user = User.objects.create_user(
            email=email, 
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        
        messages.success(request, "Registration successful.")
        return redirect('clipapp:login')
    return render(request, 'clipapp/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        User = get_user_model()
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('clipapp:dashboard')
        else:
            messages.error(request, "Invalid email or password")
    
    return render(request, 'clipapp/login.html')

@login_required(login_url='clipapp:login') 
def dashboard_view(request):
    return render(request, 'clipapp/login_page.html')

@ensure_csrf_cookie
@login_required(login_url='clipapp:login')
def snippet_view(request):
    return render(request, 'clipapp/add_snippet.html')

def user_setting(request):
    return render(request, 'clipapp/users_settings.html')

# class SnippetView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         # Add the user to the request data
#         data = request.data.copy()
#         data['user'] = request.user.id
        
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


class SnippetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Add the user to the request data
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            # Combine serialized data with the redirect URL
            response_data = serializer.data
            response_data['redirect_url'] = '/dashboard/'
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
