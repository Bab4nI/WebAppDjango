from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('accounts/', include(('AuthReg.urls', 'AuthReg'), namespace = 'AuthReg')),
    path('stock/', include(('StoreHouse.urls', 'StoreHouse'), namespace='StoreHouse')),
]
