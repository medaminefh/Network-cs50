import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .models import User, Tweet, Profile, Likes


def index(request):
    tweets = Tweet.objects.all().order_by("-created_at").all()
    likes = Likes.objects.all()

    tweets = Paginator(tweets, 10)

    page_obj = None
    try:
        page_number = request.GET.get('page')
        page_obj = tweets.get_page(page_number)

    except:
        page_obj = tweets.get_page(1)

    try:
        user = User.objects.get(username=request.user)
    except:
        user = None

    output = []

    for tweet in page_obj:
        liked = ""
        try:
            liked = likes.get(user=user, tweet=tweet)
        except:
            liked = None
        output.append({
            "id": tweet.id,
            "tweet": tweet,
            "likes": likes.filter(tweet=tweet).count(),
            "isLiked": True if liked else False
        })

    if request.method == "POST":

        # Find a way to not sending all the Page_obj TODO

        content = request.POST.get("content")
        if not user:
            return render(request,
                          "network/index.html", {"tweets": output,
                                                 "msg": "You Should Be logged in to create a Tweet", "page_obj": page_obj})
        if not content:
            return render(request,
                          "network/index.html", {"tweets": output,
                                                 "msg": "Tweet can't be Empty", "page_obj": page_obj})
        newTweet = Tweet.objects.create(content=content, user=user)
        newTweet.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "network/index.html", {"tweets": output, "page_obj": page_obj})


def profile(req, username):

    try:
        user = User.objects.get(username=username)

        profile = Profile.objects.get(user=user)
        tweets = Tweet.objects.filter(user=user).order_by("-created_at")

        tweets = Paginator(tweets, 10)

        isFollowed = None

        if req.user.is_authenticated and req.user != user:

            if req.user in profile.followers.all():
                isFollowed = True
            else:
                isFollowed = False

        page_obj = None
        try:
            page_number = req.GET.get('page')
            page_obj = tweets.get_page(page_number)
        except:
            page_obj = tweets.get_page(1)

        output = {
            "id": profile.id,
            "user": user,
            "isFollowed": isFollowed,
            "count": tweets.count,
            "tweets": page_obj,
            "followersCount": profile.followers.all().count(),
            "followingsCount": profile.following.all().count(),
            "followers": profile.followers.all(),
            "followings": profile.following.all()
        }

        return render(req, "network/profile.html", {"output": output})
    except:
        return render(req, "network/profile.html", {"msg": "User Not Exist"})


def followers(req, userid):
    try:
        profile = Profile.objects.get(user=User.objects.get(pk=userid))

        return render(req, "network/followers.html", {"followers": profile.followers.all()})

    except Exception as e:
        print(e)
        return JsonResponse({"err": "There is something wrong!"}, safe=False)


def followings(req, userid):
    try:
        profile = Profile.objects.get(user=User.objects.get(pk=userid))

        return render(req, "network/followings.html", {"followings": profile.following.all()})

    except Exception as e:
        print(e)
        return JsonResponse({"err": "There is something wrong!"}, safe=False)


@login_required(login_url="/index")
def follow(req, userid):

    if(req.method == "PUT"):

        try:
            user = User.objects.get(pk=userid)

            if req.user != user:
                profile = Profile.objects.get(user=user)
                # the profile of the logged in user
                userProfile = Profile.objects.get(user=req.user)

            if user in userProfile.following.all():
                userProfile.following.remove(user)
                profile.followers.remove(req.user)
                return JsonResponse({"msg": f"You Unfollowed {user.username} ! "}, status=200)
            else:
                userProfile.following.add(user)
                profile.followers.add(req.user)
                return JsonResponse({"msg": f"You followed {user.username} ! "}, status=200)

        except Exception as e:
            print("error in Following:", e)
            return JsonResponse({"err": "something wrong"})


def like(req, tweetid):
    if(req.method == "PUT"):

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


@login_required(login_url="/index")
def tweet(req, tweetid):
    try:
        if req.method == "PUT":
            body_unicode = req.body.decode('utf-8')
            body = json.loads(body_unicode)
            content = body['content']
            if not content:
                return JsonResponse({"error": "Tweet Can't be Empty!"})
            tweet = Tweet.objects.get(pk=tweetid)

            if content:
                tweet.content = content
                tweet.save(update_fields=["content"])
                return JsonResponse({"msg": f"Tweet {tweetid} is modified!"})
        return JsonResponse({"error": "PUT reqs only!"})
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Something went wrong with editing Post"})


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
            profile = Profile.objects.create(user=user)
            user.save()
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url="/index")
def followingposts(req):

    try:
        user = req.user
        followings = Profile.objects.get(user=user).following.all()

        tweets = Tweet.objects.filter(
            user__in=followings).order_by("-created_at").all()
        likes = Likes.objects.filter(tweet__in=tweets)

        tweets = Paginator(tweets, 10)

        page_obj = None
        try:
            page_number = req.GET.get('page')
            page_obj = tweets.get_page(page_number)

        except:
            page_obj = tweets.get_page(1)

        output = []

        for tweet in page_obj:
            liked = ""
            try:
                liked = likes.get(user=user, tweet=tweet)
            except:
                liked = None
            output.append({
                "id": tweet.id,
                "tweet": tweet,
                "likes": likes.filter(tweet=tweet).count(),
                "isLiked": True if liked else False
            })
        return render(req, "network/followingstweets.html", {"tweets": output, "page_obj": page_obj})

    except Exception as e:
        print(e)
        return JsonResponse({"error": "Something went wrong!"})
