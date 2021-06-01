from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# from Django_Agenda.settings import EMAIL_HOST_USER
# from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string

from .forms import LoginForm, RegisterForm, EditProfileForm
from agenda.models import Agenda

User = get_user_model()


def register_view(request):

    if request.user.is_authenticated:
        return redirect('/')

    form = RegisterForm(request.POST or None)

    if form.is_valid():
        first_name = form.cleaned_data.get("first_name")
        surname = form.cleaned_data.get("surname")
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")

        try:
            user = User.objects.create_user(username, email)
            user.first_name = first_name
            user.last_name = surname
            # set temporary password
            user.password = get_random_string()
            user.save()

        except Exception:  # this exception is too broad
            user = None
        """
        TO DO: add number of attempts here
        """
        if user is not None:
            # login(request, user)
            # subject = "Welcome to Django Agenda"
            # message = 'Here is a link to set your password'
            # # message = render_to_string('registration/set_password_email.html')
            # recipient = email
            # send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False)
            return redirect("/password_reset")
        else:
            request.session['register_error'] = 1  # 1 == True
            return render(request, "forms.html", {"form": form})

    return render(request, "forms.html", {"form": form})


def login_view(request):

    if request.user.is_authenticated:
        return redirect('/')

    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:  # now request.user == user until the session ends
            login(request, user)
            return redirect("/")

        else:

            # attempt = request.session.get("attempt") or 0
            # request.session['attempt'] = attempt + 1
            # return redirect("/invalid-password")
            request.session['invalid_user'] = 1  # 1 == True
            return render(request, "forms.html", {"form": form})

    return render(request, "forms.html", {"form": form})


def profile_view(request, username):
    user = User.objects.get(username=username)
    if user == request.user:
        qs = Agenda.objects.filter(user=user).order_by('-last_modified', 'entry_date')
    else:
        qs = Agenda.objects.filter(user=user).filter(public=1).order_by('-last_modified', 'entry_date')
    paginator = Paginator(qs, 5)
    page = request.GET.get('page')
    agendas = paginator.get_page(page)

    return render(request, 'account/profile.html', {'agendas': agendas, 'user': user})


@login_required
def profile_edit_view(request, username):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # need configuration for this
            # messages.success(request, 'Your Profile has been updated!')
            return redirect('profile', username)

    else:
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'forms.html', context)


def logout_view(request):
    logout(request)  # request.user = Anon User
    return redirect("/login")
