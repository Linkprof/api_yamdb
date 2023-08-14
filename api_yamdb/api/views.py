from django.shortcuts import render

from statistics import mean
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from reviews.models import Reviews, Titles

from api.serializers import CommentsSerializer, ReviewsSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = ('''IsAdminModeratorOwnerOrReadOnly,''')

    def create_or_update(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)
        ratings = Reviews.objects.filter(title=title.id)
        title.rating = round(mean([r.score for r in ratings]))
        title.save()

    def get_title(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Titles, id=title_id)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        self.create_or_update(serializer)



class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = ('''IsAdminModeratorOwnerOrReadOnly,''')

    def get_review(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Titles, id=title_id)
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(title.reviews, id=review_id)

    def get_queryset(self):
        title = self.get_review()
        return title.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)

