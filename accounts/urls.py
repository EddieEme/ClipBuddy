# from django.urls import path
# from django.contrib.auth import views as auth_views

# app_name = 'accounts'

# urlpatterns = [
#     path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset'),
#     path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
#     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
# ]