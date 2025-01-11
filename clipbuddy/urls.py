from django.contrib import admin
from django.urls import path, include
from clipapp import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('clipapp.urls', namespace='clipapp')),
    path('accounts/login/', views.login_view, name='account_login'),
    path('accounts/signup/', views.register_view, name='account_signup'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
