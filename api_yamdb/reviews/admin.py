from django.contrib import admin
from reviews.models import Categories, Comments, Genres, Review, Title

admin.site.register(Genres)
admin.site.register(Categories)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comments)
