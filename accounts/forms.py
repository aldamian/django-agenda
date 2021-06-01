from django.contrib.auth import get_user_model
from django import forms
from django.core.validators import RegexValidator
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import AuthenticationForm

alphabetical          = RegexValidator(r'^[a-zA-Z-]*$', 'Please enter only alphabetical letters.')
alphanumeric_and_line = RegexValidator(r'^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and - are allowed.')

# implement this, there must be a more elegant solution though.
# instead of me writing all the bad/offensive usernames I can think of
non_allowed_usernames = ['abc', '1234', 'admin1234']
# check for unique email & username

# Find a way to prevent users from using temp mails?
# is there a module for such a thing?
# non_allowed_emails = ['']
"""
TO DO: validate passwords.
- implement reCAPTCHA

- bootstrap tag
- forms.'field'.bootstrap
Inherit from auth Register

- user bootstrap already made and just put my classes there
"""


User = get_user_model()


class RegisterForm(forms.Form):

    first_name = forms.CharField(max_length=50, validators=[alphabetical])
    surname = forms.CharField(max_length=50, validators=[alphabetical])
    username = forms.CharField(max_length=50, validators=[alphanumeric_and_line])
    email = forms.EmailField(max_length=255)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)  # uSeRNAme == username
        if username in non_allowed_usernames:
            raise forms.ValidationError("This is an invalid username, please pick another.")
        if qs.exists():
            # We don't want people to know that an username is already taken
            raise forms.ValidationError("This is an invalid username, please pick another.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")

        return email


class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            # add form control with bootstrap
            attrs={
                "class": "form-control",
                "id": "user-name",
                "style": "width: 200px",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            # add form control with bootstrap
            attrs={
                "class": "form-control",
                "id": "user-password",
                "style": "width: 200px",
            }
        )
    )

    # def clean(self):
    #     data = super().clean()
    #     username = data.get("username")
    #     password = data.get("password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)  # ignore uppercase/lowercase
        if not qs.exists():
            raise forms.ValidationError("This is not a valid user.")

        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")

        return password


class EditProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

    # How can I add my regex validators here?

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]
