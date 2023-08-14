from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, signup, get_token

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register('v1/users', UserViewSet, basename='users')
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewsViewSet, basename="review"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments", CommentsViewSet, basename="comment",
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', get_token),
]
