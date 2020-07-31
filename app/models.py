
from django.db import models
from django.contrib.auth.models import User


class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    logo = models.FileField(upload_to='app')
    is_favourite = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='albums', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Song(models.Model):
    song_name = models.CharField(max_length=100)
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default=False)
    audio = models.FileField(upload_to='app')

    def __str__(self):
        return self.song_name



