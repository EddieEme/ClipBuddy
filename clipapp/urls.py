from django.urls import path
from . import views
from .views import SnippetView
# from django.contrib.auth import views as auth_views


app_name = 'clipapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add_snippet/', views.snippet_view, name='snippet'),
    path('settings/', views.user_setting, name='settings'),
    path('testimonial/', views.testimonial_view, name='testimonial'),
    path('edit_snippet/<int:id>/', views.edit_view, name='edit_snippet'),
    
    
    # API endpoints
    path('api/snippets/', SnippetView.as_view(), name='snippet-list-create'),
    path('api/delete/<int:id>/', views.delete_snippet, name='delete_snippet'),
    
    
    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    
]