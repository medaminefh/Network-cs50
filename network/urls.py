
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<int:userid>", views.follow, name="follow_unfollow"),
    path("user/<str:username>", views.profile, name="profile"),
    path("tweet/<int:tweetid>", views.tweet, name="tweet"),
    path("like/<int:tweetid>", views.like, name="like"),
]
