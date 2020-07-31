from django import forms
from .models import Album, Song, User


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'title', 'logo', 'genre']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['audio', 'song_name']


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

