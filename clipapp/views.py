from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages


# Create your views here.


def index(request):
    return render(request, 'clipapp/index.html')

def home(request):
    return render(request, 'clipapp/home.html')


# Registration view
def register_view(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        
        # Get the custom user model
        User = get_user_model()
        
        # Validating the password
        if password != password1:
            messages.error(request, "Passwords do not match.")
            return render(request, 'clipapp/register.html')
        
        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "clipapp/register.html")
        
        # Creating user
        first_name = full_name.split(' ')[0]
        last_name = ' '.join(full_name.split(' ')[1:])
        
        user = User.objects.create_user(
            email=email, 
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        
        messages.success(request, "Registration successful.")
        return redirect('clipapp:login')
    return render(request, 'clipapp/register.html')
    
# Login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Get the custom user model
        User = get_user_model()

        # Use authenticate with the correct credentials
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('clipapp:dashboard')
        else:
            messages.error(request, "Invalid email or password")
    
    return render(request, 'clipapp/login.html')



def dashboard_view(request):
    
    return render(request, 'clipapp/login_page.html')
