from statistics import mean

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import CustomFilter
from api.permissions import (IsAdmin,
                             ReadOrIsAdminOnly,
                             IsAdminModeratorOwnerOrReadOnly)
from api.serializers import (CategoriesSerializer, CommentsSerializer,
                             GenresSerializer, RegistrationSerializer,
                             ReviewsSerializer, TitleSerializer,
                             TitlesSerializer, UserSerializer,
                             VerificationSerializer)
from reviews.models import Categories, Genres, Review, Title
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated],
        detail=False,
        url_path='me'
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            if not (serializer.is_valid()):
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            if serializer.validated_data.get('role'):
                if request.user.role != 'admin' or not (
                    request.user.is_superuser
                ):
                    serializer.validated_data['role'] = request.user.role
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, created = User.objects.get_or_create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email']
        )
    except IntegrityError:
        return Response(
            'Такой email или имя заняты! Выберете другой!',
            status=status.HTTP_400_BAD_REQUEST
        )

    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код для Регистрации',
        f'Код для получения токена: {confirmation_code}',
        'from@yamdb.com',
        [user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = VerificationSerializer(data=request.data)
    if not (serializer.is_valid()):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    return Response(data={'token': str(token)}, status=status.HTTP_200_OK)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [ReadOrIsAdminOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomFilter
    ordering = ('name',)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitlesSerializer
        return TitleSerializer


class CategoriesViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [ReadOrIsAdminOnly]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [ReadOrIsAdminOnly]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def create_or_update(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)
        ratings = Review.objects.filter(title=title.id)
        title.rating = round(mean([r.score for r in ratings]))
        title.save()

    def get_title(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        self.create_or_update(serializer)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_review(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(title.reviews, id=review_id)

    def get_queryset(self):
        title = self.get_review()
        return title.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
