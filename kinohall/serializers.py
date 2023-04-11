"""Serializer for kinohall app"""

from rest_framework import serializers
from kinohall.models import Movie, Hall, Session


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for the Movie model"""

    class Meta:
        """Meta class for MovieSerializer"""
        model = Movie
        fields = ['id', 'title', 'description', 'year']


class HallSerializer(serializers.ModelSerializer):
    """Serializer for the Hall model"""

    class Meta:
        """Meta class for HallSerializer"""
        model = Hall
        fields = ['id', 'name', 'seats']


class SessionSerializer(serializers.ModelSerializer):
    """Serializer for the Session model"""

    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    hall = serializers.PrimaryKeyRelatedField(queryset=Hall.objects.all())

    class Meta:
        """Meta class for SessionSerializer"""
        model = Session
        fields = ['id', 'start_time', 'end_time', 'start_date', 'end_date',
                  'price', 'hall', 'movie']
