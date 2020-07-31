from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import AlbumForm, SongForm, UserForm, User, Album, Song
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .serializers import *
from rest_framework import mixins, generics, viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class IsSongOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.album.user == request.user


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


#api views


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'albums': reverse('album-list', request=request, format=format),
        'songs': reverse('song-list', request=request, format=format)
    })


class Song(viewsets.ModelViewSet):

    serializer_class = SongSerializer
    queryset = Song.objects.all()
    permission_classes = [IsSongOwnerOrReadOnly, ]


class Album(viewsets.ModelViewSet):

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsOwnerOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class User(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly, ]





#normal views

@login_required(login_url='/music/login/')
def index(request):
    albums = Album.objects.filter(user=request.user)
    query = request.GET.get('q','')
    if query:
        albums = albums.filter(Q(title__contains=query)| Q(artist__contains=query)).distinct()
        songs = Song.objects.filter(Q(song_name__contains=query)).distinct()
        context = {
            'songs': songs,
            'albums': albums
        }
        return render(request, 'app/index.html', context)

    else:
        return render(request, 'app/index.html', {'albums': albums})


@login_required(login_url='/music/login/')
def album_creation(request):
    form = AlbumForm(request.POST or None,
                     request.FILES or None)
    print('b')

    if form.is_valid():
        album = form.save(commit=False)
        album.user = request.user
        title = form.cleaned_data.get('title')
        album.logo = request.FILES['logo']
        logo = album.logo.url.split('.')[-1].lower()
        print('a')
        if logo not in IMAGE_FILE_TYPES:
            context = {
                'error_message': 'file type not supported',
                'form': AlbumForm(instance=album)
            }
            return render(request, 'app/create_album.html', context)

        album.save()
        messages.success(request, f'{title} is created')
        print('c')
        return render(request, 'app/detail.html', {'album': album})

    print('d')

    return render(request, 'app/create_album.html', {'form':AlbumForm()})


@login_required(login_url='/music/login')
def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    context = {
        'album': album,
        'user': request.user
    }
    return render(request, 'app/detail.html', context)


@login_required(login_url='/music/login/')
def delete_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    album.delete()
    return redirect('app:index')


@login_required(login_url='/music/login/')
def create_song(request, album_id):
    print('a')
    album = get_object_or_404(Album, pk=album_id)
    form = SongForm(request.POST or None,
                    request.FILES or None)

    if form.is_valid():
        print('b')
        song = form.save(commit=False)
        song.album = album
        name = song.song_name
        song.audio = request.FILES["audio"]
        extension = song.audio.url.split('.')[-1]  #Important form.cleaned_data.get('audio').url.split(.')[-1]
        if extension not in AUDIO_FILE_TYPES:       ## is wrong !!!
            context = {
                'error_message': 'file type not supported',
                'form': form,
                'album': album
            }
            return render(request, 'app/create_song.html',  context)

        song.save()
        messages.success(request, f'{name} is created in{album.title} album')
        return redirect('app:index')


    else:
        print('c')
        return render(request, 'app/create_song.html', {'form': form,
                                                        'album': album})


@login_required(login_url='/music/login/')
def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = get_object_or_404(Song, pk=song_id)
    name = song.song_name
    song.delete()
    album.save()
    messages.success(request, f'{name} is deleted!!')
    return redirect('app:index')


@login_required(login_url='/music/login/')
def favourite_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    if song.is_favourite:
        song.is_favourite=False
    else:
        song.is_favourite=True
    song.save()
    return redirect('app:index')


@login_required(login_url='/music/login/')
def favourite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    if album.is_favourite:
        album.is_favourite = False
    else:
        album.is_favourite = True
    album.save()
    return redirect('app:index')


def register(request):

    form = UserForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username, email, password)
        user.set_password(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user.save()
            login(request, user)
            albums = Album.objects.filter(user=request.user)
            context = {'albums': albums}
            print('NOtns,djbjssdc ')
            return render(request, 'app/index.html', context)
        else:
            return render(request, 'app/login.html', {'error_message': 'account disabled'})

    else:
        form = UserForm()
        context = {'form': form}
        return render(request, 'app/register.html', context)


def login_user(request):
    print(request.user)
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print('logged in')
            albums = Album.objects.filter(user=request.user)
            context = {'albums': albums}
            print('NOtns,djbjssdc ')
            return render(request, 'app/index.html', context)
        else:
            return render(request, 'app/login.html', {'error_message': 'Invalid lOGIN'})

    return render(request, 'app/login.html')


@login_required(login_url='/music/login/')
def logout_user(request):
    logout(request)
    return render(request, 'app/login.html')


@login_required(login_url='/music/login/')
def song(request, filter_by):
    albums = Album.objects.filter(user=request.user)
    songs = []

    songs = Song.objects.filter(album__in=albums)

    if filter_by == 'favorites':
        songs = songs.filter(is_favourite=True)
    return render(request, 'app/songs.html', {'songs': songs,
                                              'filter_by': filter_by})

