from django import forms

from .models import Agenda


class AgendaModelForm(forms.ModelForm):
    """
    can use these to overwrite
    can also add additional fields here
    title = forms.CharField()
    can use custom validators directly here
    """
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your title here.'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Maximum 5 tags.'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(AgendaModelForm, self).__init__(*args, **kwargs)
        self.fields['notify_me_at'].widget.attrs['disabled'] = 'true'

    """
    USE BOOTSTRAP HERE
    DECLARE ATTRIBUTES AND ADD A HTML CLASS
    or django crispy forms
    WRITE THE CSS CLASS INSIDE OF THE FIELD
    """

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
            raise forms.ValidationError("This is not long enough")
        return data

    def clean_entry_date(self):
        data = self.cleaned_data.get('entry_date')
        qs = Agenda.objects.filter(user=self.request.user, entry_date=data)
        if qs:
            raise forms.ValidationError("Can't have multiple entries on the same day.")
        return data

    def clean_notify_me_at(self):
        data1 = self.cleaned_data.get('notify_me')
        data2 = self.cleaned_data.get('notify_me_at')
        print(data1)
        if data1:
            return data2
        return None
