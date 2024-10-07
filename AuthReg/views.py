from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import Token

from .forms import SignUpForm, LoginForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from .models import Invitation
from django.urls import reverse

from .serializers import LoginSerializer


@login_required
def get_user_details(request):
    user = request.user
    user_data = {
        "surname": user.surname,
        "name": user.name,
        "patronymic": user.patronymic,
        "email": user.email,
        "role": "admin" if user.is_company_admin else "employee"
    }
    return JsonResponse(user_data)

@login_required
def get_company_details(request):
    company = request.user.company
    if company:
        company_data = {
            "name": company.name,
            "adminFamily": company.admin.surname,
            "adminName": company.admin.name,
            "adminPatronymic": company.admin.patronymic,
        }
        return JsonResponse(company_data)
    else:
        return JsonResponse({"error": "Компания не найдена"}, status=404)

def index(request):
    return render(request, 'mainTempaltes/index.html')

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'user created'
            return redirect('AuthReg:login_view')
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request,'AuthReg/page2.html', {'form': form, 'msg': msg})


@api_view(['POST'])
def login_to_mobile(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']
        # Аутентификация пользователя
        login(request, user)

        # Получаем или создаем токен для пользователя
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key
        }, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            
            if user is not None:
                auth_login(request, user)
                return redirect(reverse('mainTempaltes:index'))
            else:
                msg = 'Invalid credentials. Please try again.'
        else:
            msg = 'error validating form'

    return render(request, 'AuthReg/login.html', {'form': form, 'msg': msg})

def admin(request):
    return render(request,'admin.html')

def employee(request):
    return render(request,'employee.html')

def create_invitation(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        role = request.POST.get('role')
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

