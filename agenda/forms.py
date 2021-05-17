from django import forms

from .models import Agenda


# class AgendaForm(forms.Form):
# title = forms.CharField()


class AgendaModelForm(forms.ModelForm):
    # can use these to overwrite
    # can also add additional fields here
    # title = forms.CharField()
    # can use custom validators directly here
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
            'agenda_visibility',
            'tags',
            'notify_me',
            'notify_me_at',
            'content',
        ]

    def clean_title(self):
        data = self.cleaned_data.get('title')
        if len(data) < 4:
            raise forms.ValidationError("This is not long enough")
        return data
