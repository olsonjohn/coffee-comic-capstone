from django.contrib import admin
from ComicBaseApp.models import ComicUser, ComicBook, ComicComment, Hold


@admin.register(ComicUser)
class ComicUserAdmin(admin.ModelAdmin):
    fields = 'username', 'password', 'display_name', 'bio', 'holds','favorites', 'created_date', 'email', 'checkedout_comic'


admin.site.register(ComicBook)
admin.site.register(ComicComment)
admin.site.register(Hold)