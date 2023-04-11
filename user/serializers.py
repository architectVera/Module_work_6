"""Serializer for user app"""

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserModelSerializer(serializers.ModelSerializer):
    """Serializer for the User model"""

    class Meta:
        """A inner class that defines metadata for the serializer, such as
         the model to use and the fields to include in the serialized representation."""

        model = get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        """ The `create` method of this serializer is overridden to handle creating
        new user instances. It first removes the`password` field from the `validated_data`
        dictionary and hashes it using the `make_password` function from Django's
        `contrib.auth.hashers` module. It then calls the parent `create` method to create
         the user instance and return it."""

        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        user = super().create(validated_data)
        return user
