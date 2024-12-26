from django.urls import path
from . import views
from .views import SnippetView

app_name = 'clipapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add_snippet/', views.snippet_view, name='snippet'),
    path('settings/', views.user_setting, name='settings'),
    
    # API endpoints
    path('api/snippets/', SnippetView.as_view(), name='snippet-list-create'),
]