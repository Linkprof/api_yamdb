from rest_framework import filters, mixins, viewsets
from api.permissions import ReadOrIsAdminOnly

class CustomViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [ReadOrIsAdminOnly]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'