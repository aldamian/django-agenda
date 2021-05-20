from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm

User = get_user_model()


def register_view(request):
    # import ipdb
    # ipdb.set_trace()
    if request.user.is_authenticated:
        return redirect('/')
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        first_name  = form.cleaned_data.get("first_name")
        surname     = form.cleaned_data.get("surname")
        username    = form.cleaned_data.get("username")
        email       = form.cleaned_data.get("email")
        try:
            user = User.objects.create_user(username, email)
            user.first_name = first_name
            user.last_name  = surname
            user.save()
        except Exception:  # this exception is too broad
            user = None
        """
        TO DO: add number of attempts here
        """
        if user is not None:
            # login(request, user)
            return redirect("/email_sent")
        else:
            request.session['register_error'] = 1  # 1 == True
            return render(request, "forms.html", {"form": form})

    return render(request, "forms.html", {"form": form})


def login_view(request):

    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # now request.user == user until the session ends
            login(request, user)
            return redirect("/")
        else:
            # attempt = request.session.get("attempt") or 0
            # request.session['attempt'] = attempt + 1
            # return redirect("/invalid-password")
            request.session['invalid_user'] = 1  # 1 == True
            return render(request, "forms.html", {"form": form})
    return render(request, "forms.html", {"form": form})


def logout_view(request):
    logout(request)
    # request.user = Anon User
    return redirect("/login")
