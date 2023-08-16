from django.contrib import admin
from reviews.models import Categories, Comments, Genres, Reviews, Titles

admin.site.register(Genres)
admin.site.register(Categories)
admin.site.register(Titles)
admin.site.register(Reviews)
admin.site.register(Comments)
