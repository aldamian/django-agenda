from django.contrib.auth import get_user_model
from django import forms
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
alphanumeric_and_line = RegexValidator(r'^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and - are allowed.')

# implement this, there must be a more elegant solution though.
# instead of me writing all the bad/offensive usernames I can think of
non_allowed_usernames = ['abc']
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
    first_name  = forms.CharField(max_length=50, validators=[alphanumeric])
    surname     = forms.CharField(max_length=50, validators=[alphanumeric])
    username    = forms.CharField(max_length=50, validators=[alphanumeric_and_line])
    email       = forms.EmailField(max_length=255)

    # password1 = forms.CharField(
    #     label='Password',
    #     widget=forms.PasswordInput(
    #         # add form control with bootstrap
    #         attrs={
    #             "class": "form-control",
    #             "id": "user-password",
    #         }
    #     )
    # )
    # password2 = forms.CharField(
    #     label='Confirm Password',
    #     widget=forms.PasswordInput(
    #         # add form control with bootstrap
    #         attrs={
    #             "class": "form-control",
    #             "id": "user-confirm-password"
    #         }
    #     )
    # )

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
    username = forms.CharField()
    password = forms.CharField()

    # password = forms.CharField(
    #     widget=forms.PasswordInput(
    #         # add form control with bootstrap
    #         attrs={
    #             "class": "form-control",
    #             "id": "user-password",
    #         }
    #     )
    # )

    # def clean(self):
    #     data = super().clean()
    #     username = data.get("username")
    #     password = data.get("password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)  # ignore uppercase/lowercase
        if qs.exists():
            raise forms.ValidationError("This is not a valid user.")

        return username
