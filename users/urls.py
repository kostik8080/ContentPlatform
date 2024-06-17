from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import TemplateView

from users.apps import UsersConfig
from users.views import UserRegisterView, UserUpdateView, UserDeleteView, activate

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('password_reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        email_template_name='users/password_reset_email.html',
        success_url=reverse_lazy('users:password_reset_done'), ),
         name='password_reset'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url=reverse_lazy('users:password_reset_complete'), ),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('register_info/', TemplateView.as_view(template_name='users/register_info.html'), name='register_info'),
    path('register_done/', TemplateView.as_view(template_name='users/register_done.html'), name='register_done'),
    path('register_error/', TemplateView.as_view(template_name='users/register_error.html'),
         name='register_error'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='delete'),
]
