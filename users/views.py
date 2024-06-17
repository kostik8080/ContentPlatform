from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, DeleteView

from users.forms import UserRegisterForm, UserUpdateForm, PasswordForm
from users.models import User
from users.services import get_vrification
from users.token import account_activation_token


class UserRegisterView(CreateView):
    model = User
    form_class = (
        UserRegisterForm)
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:register_info')

    def form_valid(self, form):
        # Сохранение пользователя
        user = form.save(commit=False)
        get_vrification(self.request, user)

        return super().form_valid(form)

    def form_invalid(self, form):
        form = UserRegisterForm
        return super().form_invalid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('menenger:home')


class UserPasswordReset(PasswordResetConfirmView):
    form_class = PasswordForm
    success_url = reverse_lazy("users:password_reset_complete")
    template_name = "users/password_reset_confirm.html"



def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True

        user.save()

        #group = Group.objects.get(name='Право на изменение')
        #user.groups.add(group)
        return redirect(reverse('users:register_done'))
    else:
        return redirect(reverse('users:register_error'))
