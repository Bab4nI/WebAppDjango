from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'AuthReg'
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),        # авторизация через мобилу (возвращается токен, который в дальнейшем используется в HTML)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', views.UserDetailsAPI.as_view(), name='get_user_details'),          # данные об юзере
    path('api/company/', views.CompanyDetailsAPI.as_view(), name='get_user_details'),     # данные о компании


    path('', views.index, name = 'index'),
    path('page2/', views.register, name = 'page2'),
    path('login/', views.login, name='login'),
    path('invite/', views.create_invitation, name = 'invite'),
    path('adminpage/', views.admin, name='adminpage'),
    path('employee/', views.employee, name='employee'),
    path('register/<uuid:token>/', views.register_by_invitation, name = 'register'),
]