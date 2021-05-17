from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone


def default_notify_time():
    now = timezone.now()
    start = now.replace(hour=6, minute=0, second=0, microsecond=0)
    # user tomorrow 9 PM if the model instance is created after 9 PM
    return start if start > now else start + timedelta(days=1)


class Agenda(models.Model):
    # use sets because sets are very fast. Can't use sets, it has to be a tuple
    VISIBILITY_CHOICES = (
        ("private", "private"),
        ("public", "public")
    )
    """
    CAN USE CUSTOM VALIDATORS DIRECTLY ON ANY OF THE MODEL FIELDS
    """
    # id = models.AutoField()

    # name of the Agenda
    title = models.CharField(max_length=100, default="My Agenda")

    # set the field to when the Agenda was first created
    entry_date = models.DateField(default=timezone.now, auto_now_add=False)

    # set to when the Agenda was first created, updates when the Agenda is modified
    last_modified = models.DateField(auto_now=True, auto_now_add=False)

    # tags - search Agendas using tags
    # implement a list of default tags
    tags = models.CharField(max_length=10, default="My Tag")

    # agenda visibility, default is private
    agenda_visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES, default="private")

    # textul intrarii - ce informatie pun in agenda?
    """ 
    add markdown support - pip install django-markdown-view - DO TODAY
    https://github.com/trentm/django-markdown-deux
    https://stackoverflow.com/questions/23031406/how-do-i-implement-markdown-in-django-1-6-app
        
    """
    content = models.TextField(default="Enter your text here")

    # notify user about... about what?
    notify_me = models.BooleanField(default=False)

    # notify_me about something at a specific time, if notify me is selected
    """ 
    TO DO notificare prin email daca Notify me este selectat
    """
    notify_me_at = models.DateTimeField(default=default_notify_time())

    # create user class and modify here
    """
    added_by (user-ul care adauga intrarea in agenda)
    """
