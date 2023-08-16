from django.shortcuts import get_object_or_404
from django.core.validators import (RegexValidator)
from rest_framework import serializers
from rest_framework.validators import ValidationError

from reviews.models import Categories, Comments, Genres, Review, Title
from users.models import User

VALID_NAME = RegexValidator(r'^[\w.@+-]+\Z')


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        exclude = ('id', )


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        exclude = ('id', )


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Categories.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genres.objects.all(),
                                         many=True)
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = '__all__'


class ReadTitleSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
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

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        title = get_object_or_404(
            Title,
            pk=self.context['view'].kwargs.get('title_id'))
        if request.method == 'POST':
            if Review.objects.filter(title=title,
                                     author=request.user).exists():
                raise ValidationError('No!')
        return data


class VerificationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=250)
