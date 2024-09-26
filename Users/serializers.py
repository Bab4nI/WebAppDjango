from rest_framework import serializers

from Users.models import UserProfileModel


class UserProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = ['first_name', 'last_name', 'middle_name', 'email', 'phone_number', 'password', 'role']