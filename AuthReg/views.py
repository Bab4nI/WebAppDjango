from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login

def index(request):
    return render(request, 'AuthReg/index.html')

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

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('AuthReg:admin')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('AuthReg:employee')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'AuthReg/login.html', {'form': form, 'msg': msg})

def admin(request):
    return render(request,'admin.html')

def employee(request):
    return render(request,'employee.html')