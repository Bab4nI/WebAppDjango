from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm
from django.core.mail import send_mail
from django.contrib.auth import login as auth_login, get_user_model
from .models import Invitation
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import authenticate, login
from .serializers import UserLoginSerializer, CompanyDetailsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserDetailsSerializer



#--------------------------------------------------------------------------------------------------
class UserLoginAPI(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request)  #
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
    permission_classes = [IsAuthenticated]

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

#--------------------------------------------------------------------------------------------------

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

