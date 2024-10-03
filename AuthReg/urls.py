from django.urls import path
from . import views

app_name = 'AuthReg'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('page2/', views.register, name = 'page2'),
    path('login/', views.login, name='login'),
    path('invite/', views.create_invitation, name = 'invite'),
    path('adminpage/', views.admin, name='adminpage'),
    path('employee/', views.employee, name='employee'),
    path('register/<uuid:token>/', views.register_by_invitation, name = 'register'),
]