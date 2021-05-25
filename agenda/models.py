from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# User = settings.AUTH_USER_MODEL
User = get_user_model()


def default_notify_time():
    now = timezone.now()
    start = now.replace(hour=9, minute=0, second=0, microsecond=0)
    return start


class Agenda(models.Model):
    """
    CAN USE CUSTOM VALIDATORS DIRECTLY ON ANY OF THE MODEL FIELDS
    """
    # Foreign Key correlates 2 tables together. Correlates Agenda to User
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    # id = models.AutoField()
    # name of the Agenda
    title = models.CharField(max_length=100)
    # set the field to when the Agenda was first created
    entry_date = models.DateField(default=timezone.now)

    # set to when the Agenda was first created, updates when the Agenda is modified
    last_modified = models.DateField(auto_now=True)

    # tags - search Agendas using tags
    # implement a list of default tags, but also let the user create custom tags
    # TO DO - search by tags
    tags = models.CharField(max_length=10)

    # agenda visibility, default is private
    # keep this as to not delete the database, it isn't used.
    public = models.BooleanField(default=False)
    # entry text - what kind of info?
    """ 
    add markdown support - pip install django-markdown-view - DO TODAY
    https://github.com/trentm/django-markdown-deux
    https://stackoverflow.com/questions/23031406/how-do-i-implement-markdown-in-django-1-6-app      
    """
    # need markdown support for this
    content = models.TextField()

    # notify user about... about what?
    notify_me = models.BooleanField(default=False)

    # notify_me about something at a specific time, if notify me is selected
    """ 
    TO DO notification via email if notify_me is selected
    """
    # this should be time field
    notify_me_at = models.TimeField(default=default_notify_time, null=True, blank=True)
