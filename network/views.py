from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Tweet, Profile, Likes


def index(request):
    tweets = Tweet.objects.all().order_by("-created_at").all()
    likes = Likes.objects.all()

    print(likes)
    try:
        user = User.objects.get(username=request.user)
    except:
        user = None

    output = []

    for tweet in tweets:
        liked = ""
        try:
            liked = likes.get(user=user, tweet=tweet)
        except:
            liked = None
        output.append({
            "tweet": tweet,
            "likes": likes.filter(tweet=tweet).count(),
            "isLiked": True if liked else False
        })

    if request.method == "POST":
        content = request.POST.get("content")
        if not user:
            print("Not a user!")
            return render(request,
                          "network/index.html", {"tweets": tweets,
                                                 "msg": "You Should Be logged in to create a post"})

        newTweet = Tweet.objects.create(content=content, user=user)
        newTweet.save()
        return HttpResponseRedirect(reverse("index"))

    print(output, user)
    return render(request, "network/index.html", {'tweets': output})


def profile(req, username):
    return HttpResponse({"res": "Hello world! Profile page"})


def follow(req, userid):
    return HttpResponse({"res": "Hello world! Follow page"})


def like(req, tweetid):

    if req.user.is_authenticated:
        tweet = Tweet.objects.get(pk=tweetid)
        user = User.objects.get(username=req.user.username)

        try:
            tweetLiked = Likes.objects.get(tweet=tweet, user=user)
        except:
            tweetLiked = None

        if tweetLiked:
            tweetLiked.delete()
            return JsonResponse({"Success": "Disliked"}, status=200)

        tweetLiked = Likes.objects.create(user=user, tweet=tweet)
        tweetLiked.save()

        return JsonResponse({"Success": "Liked Succussfully"}, status=200)

    return JsonResponse({"error": "You're Not Logged In!"}, status=400)


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
