from django.urls import path
from . import views

app_name = 'AuthReg'
urlpatterns = [
    path('', views.index, name = 'index'),
    #path('invite/', views.create_invitation, name = 'invite'),
    path('create_invitation', views.create_invitation, name = 'create_invitation'),
    path('registration/<uuid:token>/', views.register_by_invitation, name = 'registration'),
    path('sucsessful_registration', views.registr, name = 'registr'),
    path('authorisation/', views.authorisation, name = 'authorisation'),
    path('account/', views.account, name = 'account'),
]

