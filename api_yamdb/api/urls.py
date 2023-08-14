from rest_framework import routers
from django.urls import include, path

from api.views import CommentsViewSet, ReviewsViewSet

router_v1 = routers.DefaultRouter()

router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewsViewSet, basename="review"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments", CommentsViewSet, basename="comment",
)