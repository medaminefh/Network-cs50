from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Tweet, Profile


def index(request):
    tweets = Tweet.objects.all().order_by("-created_at").all()
    try:
        user = User.objects.get(username=request.user)
    except:
        user = None

    if request.method == "POST":
        content = request.POST.get("content")
        if not user:
            print("Not a user!")
            return render(request, "network/index.html", {"tweets": tweets,
                                                          "msg": "You Should Be logged in to create a post"
                                                          })

        newTweet = Tweet.objects.create(content=content, user=user)
        newTweet.save()
        return HttpResponseRedirect(reverse("index"))

    print(tweets, user)
    return render(request, "network/index.html", {'tweets': tweets})


def profile(req, username):
    return HttpResponse({"res": "Hello world! Profile page"})


def follow(req, userid):
    return HttpResponse({"res": "Hello world! Follow page"})


def like(req):

    if req.method == "POST" and req.user.is_authenticated:
        tweetId = req.POST.get("tweetId")
        user = User.objects.get(username=req.user)
        likedTweet = Tweet.objects.get(pk=tweetId)
        likedTweet.likes = user
        likedTweet.save()
        print("the tweet's id is ", tweetId)
        return HttpResponse({"Success": "Liked Succussfully"})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
