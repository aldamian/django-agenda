from django.db import models
from django.contrib.auth import authenticate, login


class Profile(models.Model):

    content = models.TextField()
    # image
    # location
    # screen name
