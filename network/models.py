from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    title = models.CharField(max_length=100)
    tweet = models.TextField()
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator")

    created_at = models.DateTimeField(auto_now_add=True)
