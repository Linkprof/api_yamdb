from rest_framework import serializers
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator)

from users.models import User
from reviews.models import Titles, Comments, Reviews
from reviews.models import Categories, Genres, Titles

VALID_NAME = RegexValidator(r'^[\w.@+-]+\Z')


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Categories.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genres.objects.all(),
                                         many=True)

    class Meta:
        model = Titles
        fields = '__all__'


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
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[VALID_NAME],)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать имя "me" для регистрации.'
            )
        return value


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField(
        validators=(
            MinValueValidator(1, 'Оценка не может быть меньше 1.'),
            MaxValueValidator(10, 'Оценка не может быть выше 10.')
        )
    )

    class Meta:
        model = Reviews
        fields = ('id', 'author', 'text', 'score', 'pub_date')


class VerificationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=250)
