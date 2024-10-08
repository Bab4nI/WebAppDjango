from django.urls import path
from . import views

app_name = 'AuthReg'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', views.login, name='login'),
    #path('invite/', views.create_invitation, name = 'invite'),
    path('registration/<uuid:token>/', views.register_by_invitation, name = 'registration'),
    path('authorisation/', views.authorisation, name = 'authorisation'),
    path('account/', views.account, name = 'account'),
    path('inventory/', views.inventory, name = 'inventory'),
]