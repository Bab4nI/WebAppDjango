from django.contrib.auth import views as auth_views
from Users import views
from django.urls import path

urlpatterns = [
    # Маршрут для регистрации уже есть
    path('addUser/', views.User_registration.as_view(), name='addUser'),
    path('getUsers/', views.User_registration.as_view(), name="getUsers"),

    # API для авторизации
    path('api/login/', views.UserLoginAPI.as_view(), name='api_login'),


    # URL для входа и выхода через веб
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


]
