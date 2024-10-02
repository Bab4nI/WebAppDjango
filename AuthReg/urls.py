from django.urls import path
from . import views

app_name = 'AuthReg'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('page2/', views.register, name = 'page2'),
    path('login/', views.login_view, name='login_view'),
    #path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('employee/', views.employee, name='employee'),
]