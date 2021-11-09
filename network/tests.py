from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Likes, Tweet, Profile, User

# Create your tests here.


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='normal@user.com', password='foo')
        self.assertEqual(user.username, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(username="")
        with self.assertRaises(ValueError):
            User.objects.create_user(username='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='super@user.com', password='foo')
        self.assertEqual(admin_user.username, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_create_tweet(self):
        user1 = User.objects.create(username="med")
        user2 = User.objects.create(username="haroun")
        user3 = User.objects.create(username="amira")

        newTweet1 = Tweet.objects.create(user=user1, content="Hello world!")
        newTweet2 = Tweet.objects.create(
            user=user2, content="Hello world! My name is Haroun")
        newTweet3 = Tweet.objects.create(
            user=user3, content="Hello world! My name is Amira")

        self.assertEqual(user1.username, 'med')
        self.assertEqual(newTweet1.user.username, 'med')
        self.assertTrue(newTweet2.content, "Hello world! My name is Haroun")
        self.assertTrue(newTweet3.content, "Hello world! My name is Amira")
        self.assertTrue(newTweet3.user, "amira")
