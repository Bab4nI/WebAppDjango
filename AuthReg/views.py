from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from .models import Invitation
from AuthReg.models import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import status
from .serializers import UserLoginSerializer, CompanyDetailsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserDetailsSerializer

def index(request):
    return render(request, 'mainTempaltes/index.html')



def create_invitation(request):
    if request.method == 'POST':   
        form = InviteForm(data = request.POST)
        if form.is_valid():  
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            company = request.user.company

            invitation = Invitation.objects.create(
                company = company,
                role = role,
                email = email
            )

            invitation_link = request.build_absolute_uri(reverse('AuthReg:registration', args=[invitation.token]))

            send_mail(
                'Приглашение на регистрацию',
                f'Пройдите по следующей ссылке для регистрации: {invitation_link}',
                'noreply@mail.ru',
                [email],
            )

            return redirect(reverse('index'))
    else:
        form = InviteForm()
    return render(request, 'AuthReg/invitationPLUG.html', {'form': form})
    
def register_by_invitation(request, token):
    invitation = get_object_or_404(Invitation, token=token)

    if not invitation.is_valid():
        return render(request, 'AuthReg/invitation_invalid.html')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            user = User.objects.create_user(
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password1'],
                name = form.cleaned_data['name'],
                surname = form.cleaned_data['surname'],
                patronymic = form.cleaned_data['patronymic'],
            )
            user.company = invitation.company
            user.is_company_admin = (invitation.role == 'admin')
            user.save()

            invitation.used = True
            invitation.save()
            return redirect('AuthReg:authorisation')
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'AuthReg/registration.html', {'invitation': invitation, 'form': form})

def registr(request):
    return render(request, 'AuthReg/registr')

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

class UserLoginAPI(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request) 
                return Response({
                    "message": "Успешный вход",
                    "user_id": user.id,
                    "email": user.email,
                    "role": "admin" if user.is_admin else "employee"
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Неверные учетные данные"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailsAPI(APIView):
    def get(self, request):
        user = request.user
        company = user.company

        if company:
            serializer = CompanyDetailsSerializer(company)
            return Response(serializer.data)
        else:
            return Response({"error": "Компания не найдена"}, status=404)


class UserDetailsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    
    

