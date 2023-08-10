from rest_framework import serializers
from django.core.validators import RegexValidator

from users.models import User


VALID_NAME = RegexValidator(r'^[\w.@+-]+\Z')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(
        regex=VALID_NAME, max_length=150, required=True
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Невозможно использовать имя "me" для регистрации.'
            )
        return value


class CreateTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=VALID_NAME, max_length=150, required=True
    )
    confirmation_code = serializers.CharField(required=True)
