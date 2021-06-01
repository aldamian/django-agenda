from Django_Agenda.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.utils import timezone

from .models import Agenda

# Needs to be optimized, otherwise it wastes a lot of resources
# especially if deployed in cloud and lots of users


def agenda_scheduled_notifications():
    import ipdb
    ipdb.set_trace()
    qs = Agenda.objects.filter(notify_me=True).filter(entry_date=timezone.now().date())
    now = timezone.now().time()
    allowed_error = now.replace(hour=0, minute=2, second=0, microsecond=0)
    for obj in qs:
        if obj.notify_me_at - timezone.now().time() <= allowed_error:
            subject = obj.title
            # Need to add it as markdown
            message = obj.content
            recipient = obj.user.email
            send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False)
