from django.contrib import admin
from django.urls import include, path
from StoreHouse import views as StoreHouse_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('stock/', include(('StoreHouse.urls', 'StoreHouse'), namespace='StoreHouse'))
]
