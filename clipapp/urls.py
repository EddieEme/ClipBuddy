from django.urls import path
from clipapp import views


urlpatterns = [
    path('', views.index, name='index'),
]
