from django.contrib import admin
from django.urls import path, include
from clipapp import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('clipapp.urls', namespace='clipapp')),
    path('accounts/login/', views.login_view, name='account_login'),
    path('accounts/signup/', views.register_view, name='account_signup'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
