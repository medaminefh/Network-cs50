from django.contrib.auth import get_user_model
from django.test import TestCase, Client, client
from .models import Likes, Tweet, Profile, User

# Create your tests here.


class UsersManagersTests(TestCase):

    # Run This function before any test, Basically we'll create users, and posts
    # setUp function is a special fn in Django, it's work is to run some things before any Test runs
    def setUp(self):
        # create users and their profiles
        user1 = User.objects.create(username="med", password="123456")
        profile1 = Profile.objects.create(user=user1)

        user2 = User.objects.create(username="medamine", password="123456")
        profile2 = Profile.objects.create(user=user2)

        user3 = User.objects.create(username="haroun", password="19971997Am")
        profile3 = Profile.objects.create(user=user3)

        tweet1 = Tweet.objects.create(user=user2, content="Hello world!")
        tweet2 = Tweet.objects.create(
            user=user1, content="Hello world from Med1!")
        tweet3 = Tweet.objects.create(
            user=user1, content="Hello world from Med2!")
        tweet4 = Tweet.objects.create(
            user=user1, content="Hello world from Med3!")

    def test_users_count(self):
        users = User.objects.all()
        """ assert that there is 3 users """
        self.assertEqual(users.count(), 3)

        """ assert that there is 3 Profiles """
        profiles = Profile.objects.all()
        self.assertEqual(profiles.count(), 3)

    def test_tweet_count(self):

        medTweets = Tweet.objects.filter(user=User.objects.get(username="med"))
        medamineTweets = Tweet.objects.filter(
            user=User.objects.get(username="medamine"))

        allTweets = Tweet.objects.all()
        self.assertEqual(allTweets.count(), 4)
        self.assertEqual(medTweets.count(), 3)
        self.assertEqual(medamineTweets.count(), 1)

    def test_followers(self):
        profile1 = Profile.objects.get(user=User.objects.get(username="med"))
        profile2 = Profile.objects.get(
            user=User.objects.get(username="medamine"))

        self.assertEqual(profile1.followers.all().count(), 0)
        self.assertEqual(profile2.followers.all().count(), 0)

    def test_index(self):
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["tweets"]), 4)
