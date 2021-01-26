from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as v


urlpatterns = [
    path('register/', v.register, name='WebApp-register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='WebApp-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='WebApp-logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='WebApp-password_reset'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete')
]
