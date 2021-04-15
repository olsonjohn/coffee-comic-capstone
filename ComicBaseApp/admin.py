from django.contrib import admin
from ComicBaseApp.models import ComicUser, ComicBook, ComicComment


@admin.register(ComicUser)
class ComicUserAdmin(admin.ModelAdmin):
    fields = 'username', 'password', 'display_name', 'bio', 'favorites', 'created_date'


admin.site.register(ComicBook)
admin.site.register(ComicComment)
