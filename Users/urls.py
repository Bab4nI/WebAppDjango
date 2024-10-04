from django.contrib.auth import views as auth_views
from Users import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API для регистрации
    path('api/register/', views.UserRegistration.as_view(), name='register'),

    # API для авторизации
    path('api/login/', views.UserLoginAPI.as_view(), name='api_login'),

    # URL для входа и выхода через веб
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
