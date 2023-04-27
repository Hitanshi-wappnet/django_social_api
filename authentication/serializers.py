from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from authentication.models import User


# Serializer for user registration
class RegistrationSerializer(serializers.ModelSerializer):

    # Use a validator to ensure email is unique
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    # Define the model and fields for the serializer
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}

    # Use a password field to ensure password is write_only and encrypted
    password = serializers.CharField(
        style={"input_type": "password", "write_only": True}
    )

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
