from django import forms
from django.utils import timezone
import datetime

from .models import Agenda


class AgendaModelForm(forms.ModelForm):
    """
    can use these to overwrite
    can also add additional fields here
    title = forms.CharField()
    can use custom validators directly here
    """
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Agenda name'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Maximum 5 tags'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(AgendaModelForm, self).__init__(*args, **kwargs)
        # self.fields['notify_me_at'].widget.attrs['disabled'] = 'true'

    """
    USE BOOTSTRAP HERE
    DECLARE ATTRIBUTES AND ADD A HTML CLASS
    or django crispy forms
    WRITE THE CSS CLASS INSIDE OF THE FIELD
    """

    def clean(self):

        entry_date = self.cleaned_data.get('entry_date')
        if entry_date is not None:
            notify_me = self.cleaned_data.get('notify_me')
            notify_me_at = self.cleaned_data.get('notify_me_at')

            min_time_diff = datetime.timedelta(hours=1)
            # need to set timezone to user timezone
            now = datetime.datetime.strptime(str(timezone.now())[0:19], "%Y-%m-%d %H:%M:%S") + 3 * min_time_diff

            enter_delta = datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
            exit_delta = datetime.timedelta(hours=notify_me_at.hour,
                                            minutes=notify_me_at.minute,
                                            seconds=notify_me_at.second)

            actual_time_diff = exit_delta-enter_delta
            # print(entry_date, notify_me_at, now.time(), min_time_diff)

            if entry_date < now.date() and notify_me:
                raise forms.ValidationError("Can't notify for entries in the past.")

            if notify_me and entry_date == now.date() and notify_me_at > now.time() and actual_time_diff < min_time_diff:
                raise forms.ValidationError("Can't notify sooner than 1 hour.")

        return self.cleaned_data

    class Meta:
        model = Agenda
        fields = [
            'title',
            'entry_date',
            'tags',
            'public',
            'notify_me',
            'notify_me_at',
            'content',
        ]

    def clean_title(self):
        data = self.cleaned_data.get('title')
        if len(data) < 4:
            raise forms.ValidationError("Title too short.")
        return data

    def clean_entry_date(self):
        data = self.cleaned_data.get('entry_date')
        qs = Agenda.objects.filter(user=self.request.user, entry_date=data)
        if qs:
            raise forms.ValidationError("Can't have multiple entries on the same day.")
        return data

    def clean_notify_me_at(self):
        data = self.cleaned_data.get('notify_me_at')
        return data
