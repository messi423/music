from django.urls import path, include
from django.conf.urls import url
from . import views as app_views
from django.contrib.auth import views as auth_views



urlpatterns = [

    path('', app_views.index, name='index'),
    path('<int:album_id>/', app_views.detail, name='detail'),
    path('songs/<str:filter_by>/', app_views.song, name='songs'),
    path('register/', app_views.register, name='register'),
    path('login/', app_views.login_user, name='login'),
    path('logout/', app_views.logout_user, name='logout'),
    path('create_album/', app_views.album_creation, name='create_album'),
    url(r'^(?P<album_id>[0-9]+)/create_song/$', app_views.create_song, name='create_song'),
    path('delete_album/<int:album_id>/', app_views.delete_album, name='delete_album'),
    path('delete_song/<int:album_id>/<int:song_id>/', app_views.delete_song, name='delete_song'),
    path('favorite_album/<int:album_id>/', app_views.favourite, name='favorite_album'),
    path('favorite/<int:song_id>/', app_views.favourite_song, name='favorite'),
]