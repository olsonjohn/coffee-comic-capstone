from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class ComicUser(AbstractUser):
    display_name = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField()
    favorites = models.ManyToManyField('ComicBook', blank=True, related_name='favorites')
    REQUIRED_FIELDS = ['display_name', 'bio']

    def __str__(self):
        return self.username


class ComicBook(models.Model):
    name = models.CharField(max_length = 150)
    author = models.CharField(max_length = 50)
    description = models.TextField()
    published_date = models.DateField()
    publisher = models.CharField(max_length = 50)
    volume = models.IntegerField()
    issue = models.IntegerField()
    is_checked_out = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.name} | {self.author} | Vol.: {self.volume} - No.: {self.issue}'