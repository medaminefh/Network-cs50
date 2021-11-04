from django.contrib import admin
from .models import User, Tweet, Profile, Likes
# Register your models here.

admin.site.register(User)
admin.site.register(Tweet)
admin.site.register(Profile)
admin.site.register(Likes)
