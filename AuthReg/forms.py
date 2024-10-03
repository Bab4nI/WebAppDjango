from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

class SignUpForm(UserCreationForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        min_length=2, 
        max_length=30, 
        error_messages={
            'min_length': {
                'required': 'Имя должно состоять минимум из 2 букв',
            },
            'max_length': {
                'required': 'Имя должно состоять максимум из 30 букв',
            },
        }
    )
    
    surname = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        min_length=2,
        max_length=30,
        error_messages={
            'min_length': {
                'required': 'Фамилия должна состоять минимум из 2 букв',
            },
            'max_length': {
                'required': 'Фамилия должна состоять максимум из 30 букв',
            },
        }
    )

    patronymic = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
        max_length=30,
        error_messages={
            'max_length': {
                'required': 'Отчество должно состоять максимум из 30 букв',
            },
        }
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        error_messages={
            'required': 'Пожалуйста, введите адрес электронной почты',
            'invalid': 'Пожалуйста, введите адрес электронной почты корректно',
        }
    )

    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('employee', 'Сотрудник'),
    ]

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control",}),
        min_length=8,
        error_messages={
            'min_length': {
                'Пароль должен состоять минимум из 8 символов'
            },
            'required': 'Пожалуйста, введите пароль',
        }
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control",}),
    )
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control",          
            }
        )
    )

    class Meta:
        model = User
        fields = ('surname', 'name', 'patronymic', 'email', 'password1', 'password2', 'role')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        return cleaned_data