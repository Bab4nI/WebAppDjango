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
    #path('invite/', views.create_invitation, name = 'invite'),
    path('create_invitation', views.create_invitation, name = 'create_invitation'),
    path('registration/<uuid:token>/', views.register_by_invitation, name = 'registration'),
    path('sucsessful_registration', views.registr, name = 'registr'),
    path('authorisation/', views.authorisation, name = 'authorisation'),
    path('account/', views.account, name = 'account'),
]

