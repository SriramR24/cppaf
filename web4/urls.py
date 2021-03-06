from django.contrib import admin
from django.urls import path, include
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('gold/', include('gold.urls')),
    path('silver/', include('silver.urls')),
    path('oil/', include('oil.urls')),
    path('gas/', include('gas.urls')),
]
