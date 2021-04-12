from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class ComicBook(models.Model):
    name = models.CharField(max_length = 150, null=True, blank=True)
    author = models.CharField(max_length = 50)
    description = models.TextField(null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    publisher = models.CharField(max_length = 50, null=True, blank=True)
    volume = models.CharField(max_length=150)
    issue = models.IntegerField()
    image = models.URLField(default="")
    is_checked_out = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.name} | {self.author} | Vol.: {self.volume} - No.: {self.issue}'


class ComicUser(AbstractUser):
    display_name = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField()
    favorites = models.ManyToManyField('ComicBook', blank=True, related_name='favorites')
    #favorites = models.ForeignKey('ComicBook', on_delete=models.CASCADE, null=True, blank=True, related_name='favorites')
    REQUIRED_FIELDS = ['display_name', 'bio']

    def __str__(self):
        return self.username


class ComicComment(models.Model):
    comic_book_title = models.ForeignKey(ComicBook, on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey(ComicUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment

