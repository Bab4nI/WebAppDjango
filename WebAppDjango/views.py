from django.shortcuts import render, redirect
from django.urls import reverse

def index(request):
    return render(request, 'mainTemplates/index.html')

def page2(request):
    return render(request, 'mainTemplates/page2.html')

def company(request):
    if request.user.is_authenticated:
        return render(request, 'mainTemplates/companyPLUG.html')
    else:
        return redirect(reverse('AuthReg:login'))