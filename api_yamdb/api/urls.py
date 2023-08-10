from rest_framework import routers
from django.urls import include, path

from .views import CommentsViewSet, ReviewsViewSet

router = routers.DefaultRouter()

router.register(
    r"", ReviewsViewSet, basename="review"
)
router.register(
    r"", CommentsViewSet, basename="comment",
)