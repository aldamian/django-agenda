from django.contrib.auth import get_user_model
from django import forms

# implement this, there must be a more elegant solution though.
# instead of me writing all the bad/offensive usernames I can think of
non_allowed_usernames = ['abc']
# check for unique email & username

# Find a way to stop users from using temp mails?
# is there a module for such a thing?
# non_allowed_emails = ['']
"""
TO DO: validate passwords.
"""
User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            # add form control with bootstrap
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )
    username = forms.CharField()
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            # add form control with bootstrap
            attrs={
                "class": "form-control",
                "id": "user-confirm-password"
            }
        )
    )

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
        qs = User.objects.filter(username__iexact=email)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")

        return email


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            # add form control with bootstrap
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )

    # def clean(self):
    #     username = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password")
    #     # verify here if the user password is correct
    #     # add additional form validation

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)  # ignore uppercase/lowercase
        if not qs.exists():
            raise forms.ValidationError("This is not a valid user.")

        return username
