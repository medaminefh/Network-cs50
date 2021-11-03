from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Tweet(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator")
    content = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name="like")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"This Tweet created by {self.user.username} and has {self.likes} Likes"

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "createdAt": self.created_at,
            "likes": self.likes.count()
        }


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(
        User, blank=True, related_name="followers")
    following = models.ManyToManyField(
        User, blank=True, related_name="following")

    def __str__(self):
        return f"This is {self.user.username}"
