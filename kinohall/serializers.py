from rest_framework import serializers
from kinohall.models import Movie, Hall
from user.models import UserModel


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'year']


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ['id', 'name', 'seats']

#
# class ArticleSerializer(serializers.ModelSerializer):
#     genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())
#     author = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())
#
#     class Meta:
#         model = Article
#         fields = ['slug', 'title', 'description', 'genre', 'author']
