from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class ComicUser(AbstractUser):
    display_name = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField()
    REQUIRED_FIELDS = ['display_name', 'bio']

    def __str__(self):
        return self.username
