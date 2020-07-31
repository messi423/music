from .models import *
from rest_framework import serializers


class SongSerializer(serializers.HyperlinkedModelSerializer):


    def __init__(self, *args, **kwargs):
        super(SongSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].method == "POST":
            self.fields['album'] = serializers.ChoiceField(
                choices=[(o.id, o.title) for o in Album.objects.filter(user=self.context['request'].user)]
            )

        if self.context['request'].method == "GET":
            self.fields['album'] = serializers.CharField(
                source='album.title'
            )

    class Meta:
        model = Song
        fields = ['id', 'audio', 'is_favourite', 'album', 'song_name']


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    songs = serializers.PrimaryKeyRelatedField(many=True, queryset=Song.objects.all())

    class Meta:
        model = Album
        fields = ['id', 'artist', 'title', 'genre', 'is_favourite', 'songs', 'user']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    albums = serializers.PrimaryKeyRelatedField(many=True, queryset=Album.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'albums']


