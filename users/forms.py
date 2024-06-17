from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.views import PasswordResetConfirmView

from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-check-input'})


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['phone', 'email', 'first_name', 'last_name', 'avatar', 'password1', 'password2']

    def clean_phone(self):
        clean_data = self.cleaned_data['phone']
        if not clean_data.startswith('+7'):
            raise forms.ValidationError('Телефон должен начинаться с "+7"')
        return clean_data





class UserUpdateForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ['phone', 'email', 'first_name', 'last_name', 'avatar',]

    def clean_phone(self):
        clean_data = self.cleaned_data['phone']
        if not clean_data.startswith('+7'):
            raise forms.ValidationError('Телефон должен начинаться с "+7"')
        return clean_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class PasswordForm(StyleFormMixin, PasswordResetConfirmView):
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)