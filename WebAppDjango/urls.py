from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('accounts/', include(('AuthReg.urls', 'AuthReg'), namespace = 'AuthReg')),
    path('stock/', include(('StoreHouse.urls', 'StoreHouse'), namespace='StoreHouse')),
    path('company/', views.company, name = 'company'),
    path('api/', include('InventoryRequests.urls')),
    path('support/', views.support, name = 'support'),
    path('app_link/', views.app_link, name = 'app_link'),
    path('support/', views.support, name = 'support'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)