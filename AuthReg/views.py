from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from .models import Invitation
from AuthReg.models import *
from django.urls import reverse

from django.contrib.auth.hashers import check_password

def index(request):
    return render(request, 'mainTempaltes/index.html')

def registration(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'user created'
            return redirect('AuthReg:login')
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request,'AuthReg/registration.html', {'form': form, 'msg': msg})

def create_invitation(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        role = request.POST.get('email')
        company = request.user.company

        invitation = Invitation.objects.create(
            company = company,
            role = role,
            email = email
        )

        invitation_link = request.build_absolute_urri(reverse('registered_by_invitation', args = [invitation.token]))

        send_mail(
            'Приглашение на регистрацию',
            f'Пройдите по следующей ссылке для регистрации: {invitation_link}',
            'noreply@yourdomain.com',
            [email],
        )

        return redirect('dashboard')
    
    return render(request, 'invitation.html')
    
def register_by_invitation(request, token):
    User = get_user_model()
    invitation = get_object_or_404(Invitation, token=token)

    if not invitation.is_valid():
        return render(request, 'invitation_invalid.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.create_user(
            username=username,
            password=password,
            company=invitation.company,
            is_company_admin=(invitation.role == 'admin')
        )

        invitation.used = True
        invitation.save()

        return redirect('login')

    return render(request, 'register_by_invitation.html', {'invitation': invitation})

def authorisation(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(f"Email: {email}, Password: {password}")  # Для диагностики
            user = authenticate(request, email=email, password=password)
            
            if user is None:
                print("authenticate вернул None")
                try:
                    found_user = User.objects.get(email=email)
                    print(f"Найден пользователь с email: {found_user}")
                    if found_user.check_password(password):
                        print("Пароль правильный, но authenticate не работает")
                    else:
                        print("Неверный пароль")
                except User.DoesNotExist:
                    print("Пользователь не найден")

            if user is not None:
                auth_login(request, user)
                return redirect('index')

        return render(request, 'AuthReg/authorisation.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'AuthReg/authorisation.html', {'form': form})

def account(request):
    if request.user.is_authenticated:
        user = request.user
        company = user.company
        if user.is_company_admin:
            role = 'admin'
        else:
            role = 'employee'
        User_context = {
            'surname': user.surname,
            'name': user.name,
            'middlename': user.patronymic,
            'email': user.email,
            'role': role,
        }

        if company:
            employees = company.employees.all()
            warehouses = company.warehouses.all()
            items = company.items.all()
            Inventory_context = {
                'company': company,
                'employees': employees,
                'warehouses': warehouses,
                'items': items,
            }
        else:
            Inventory_context = {
                'company': None,
                'employees': [],
                'warehouses': [],
                'items': [],
            }

        context = {**User_context, **Inventory_context}
        return render(request, 'AuthReg/account.html', context)

    else:
        return redirect('AuthReg:authorisation')
     
def inventory (request):
    return render(request, 'AuthReg/inventar')