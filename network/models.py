from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Tweet(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tweet N°{self.id}"

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "createdAt": self.created_at
        }


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    def __str__(self):
        return f"Like N°{self.id}"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(
        User, blank=True, related_name="followers")
    following = models.ManyToManyField(
        User, blank=True, related_name="following")

    def __str__(self):
        return f"This is {self.user.username}"
