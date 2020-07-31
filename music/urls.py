"""music URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from app import views as app_views


r1 = routers.SimpleRouter()
r1.register(r'songs', app_views.Song, basename='Song')
#r1.register(r'song/{pk}/', app_views.SongDetail, basename='Song')
r1.register(r'albums', app_views.Album, basename='Album')
#r1.register(r'albums/{pk}/', app_views.AlbumDetail, basename='Album')
r1.register(r'users', app_views.User, basename='User')
#r1.register(r'users/{pk}/', app_views.UserDetail, basename='User')

urlpatterns = [
    path('api/', include(r1.urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('music/', include(('app.urls', 'app'), namespace='music')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


