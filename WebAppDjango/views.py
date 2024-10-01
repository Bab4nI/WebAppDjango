from django.shortcuts import render, redirect

def index(request):
    return render(request, 'mainTemplates/index.html')

def page2(request):
    return render(request, 'mainTemplates/page2.html')