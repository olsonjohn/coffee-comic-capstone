from django.contrib import admin
from ComicBaseApp.models import ComicUser, ComicBook, ComicComment
# from django.contrib.auth.admin import UserAdmin
# Register your models here.

# admin.site.register(UserAdmin)


@admin.register(ComicUser)
class ComicUserAdmin(admin.ModelAdmin):
    fields = 'username', 'password', 'display_name', 'bio', 'favorites'


admin.site.register(ComicBook)
admin.site.register(ComicComment)
