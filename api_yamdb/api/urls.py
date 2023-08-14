from django.urls import include, path
from api.views import UserViewSet, signup, get_token

from rest_framework.routers import DefaultRouter

from api.views import CategoriesViewSet, GenresViewSet, TitlesViewSet


router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewsViewSet, basename="review"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments", CommentsViewSet, basename="comment",
)
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register('genres', GenresViewSet, basename='genres')
router_v1.register('titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', get_token),
]
