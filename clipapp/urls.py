from django.urls import path
from clipapp import views

app_name = 'clippapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login')
]
