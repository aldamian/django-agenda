# from django.db import models
# from django.core.validators import RegexValidator
# from django.contrib.auth.models import User

"""
Use User, define specific class only if I need something more
"""

# alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
# I'm not sure if this regex is correct
# alphanumeric_and_line = RegexValidator(r'^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and - are allowed.')


# class User(AbstractBaseUser):
#     # prevent users from creating accounts using temp mail
#     username    = models.CharField(max_length=50, blank=True, null=True, validators=[alphanumeric])
#     first_name  = models.CharField(max_length=50, blank=True, null=True, validators=[alphanumeric])
#     surname     = models.CharField(max_length=50, blank=True, null=True, validators=[alphanumeric])
#     email       = models.EmailField(max_length=255, unique=True)
#
#     """
#     TO DO: SET PASSWORD VIA EMAIL NOTIFICATION
#     Receive an user register welcome email
#     - send link via email to set password
#     - make register page
#     - add clean function in form that doesn't allow
#     """
#
#     active      = models.BooleanField(default=True)   # can login
#     staff       = models.BooleanField(default=False)  # staff user non superuser
#     admin       = models.BooleanField(default=False)  # superuser
#
#     USERNAME_FIELD = 'username'
