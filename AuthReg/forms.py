from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget= forms.TextInput(
            attrs={
                "class": "form-control",
                "required": True
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "required": True
            }
        )
    )


class SignUpForm(UserCreationForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "required": True
            }
        )
    )

    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "required": True
            }
        )
    )

    patronymic = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "required": True
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "required": True
            }
        )
    )

    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "required": True
            }
        )
    )

    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('employee', 'Сотрудник'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "required": True
            }
        )
    )

    class Meta:
        model = User
        fields = ('surname', 'name', 'patronymic', 'password1', 'password2', 'email', 'is_admin', 'is_employee')