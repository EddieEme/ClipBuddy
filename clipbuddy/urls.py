from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('clipapp.urls', namespace='clipapp')),
    # path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
