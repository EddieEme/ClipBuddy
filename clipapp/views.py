from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from .models import Snippet, UserTestimonial
from .serializers import SnippetSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseNotFound
from .forms import TestimonialForm



class SnippetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100
    

def index(request):
    return render(request, 'clipapp/index.html')

def home(request):
    testimonials_list = UserTestimonial.objects.all()
    paginator = Paginator(testimonials_list, 10)
    
    page_number = request.GET.get('page')
    testimonials = paginator.get_page(page_number)
    return render(request, 'clipapp/home.html', {'testimonials': testimonials})

@login_required
def testimonial_view(request):
    """
    If the user is not authenticated, redirect them to login.
    After login, redirect them back to this testimonial view.
    """
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(request, 'Thank you for your testimonial!')
            return redirect('clipapp:testimonial')
    else:
        form = TestimonialForm()

    return render(request, 'clipapp/testimonial.html', {'form': form})



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
        
        messages.success(request, "Registration successful. Login here")
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
    
    return render(request, 'clipapp/login.html', {'messeges': messages})



def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({"message": "Successfully logged out"}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    


@login_required(login_url='clipapp:login') 
def dashboard_view(request):
    return render(request, 'clipapp/login_page.html')

@ensure_csrf_cookie
@login_required(login_url='clipapp:login')
def snippet_view(request):
    return render(request, 'clipapp/add_snippet.html')


@login_required(login_url='clipapp:login') 
def user_setting(request):
    return render(request, 'clipapp/users_settings.html')



@login_required(login_url='clipapp:login') 
def edit_view(request, id):
    snippet = get_object_or_404(Snippet, id=id)

    if request.method == 'POST':
        # Update snippet with data from the form
        snippet.title = request.POST.get('title')
        snippet.description = request.POST.get('description')
        snippet.content = request.POST.get('content')
        snippet.favorite = request.POST.get('favorite') == 'on'
        snippet.tags = request.POST.get('tags', '').split(',')
        snippet.save()
        return redirect('clipapp:dashboard')

    return render(request, 'clipapp/edit_snippet.html', {'snippet': snippet})


# ..............................................APIs........................................................
class SnippetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            response_data = serializer.data
            response_data['redirect_url'] = '/dashboard/'
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request):
        snippets = Snippet.objects.filter(user=request.user).order_by('-created_at')
        paginator = SnippetPagination()
        paginated_snippets = paginator.paginate_queryset(snippets, request)
        serializer = SnippetSerializer(paginated_snippets, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    
@login_required
@require_http_methods(["DELETE"])
def delete_snippet(request, id):
    """
    View to delete a snippet by ID.
    Only allows deletion if the user owns the snippet.
    """
    try:
        snippet = get_object_or_404(Snippet, id=id, user=request.user)
        snippet.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Snippet successfully deleted'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)