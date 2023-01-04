from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        models = User
        fields= (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password2'
        )