from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'ename', 'esalary', 'username', 'phone_number', 'gender', 'hobbies','address','isDeleted']
