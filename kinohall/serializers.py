
from rest_framework import serializers
from kinohall.models import Movie, Hall, Session
from user.models import UserModel


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'year']


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ['id', 'name', 'seats']


class SessionSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    hall = serializers.PrimaryKeyRelatedField(queryset=Hall.objects.all())

    class Meta:
        model = Session
        fields = ['id', 'start_time', 'end_time', 'date', 'price', 'hall', 'movie']

