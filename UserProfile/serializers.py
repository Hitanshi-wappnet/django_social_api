from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from authentication.models import User


class ChangeProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
