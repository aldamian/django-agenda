from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from Django_Agenda.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.template.loader import render_to_string

# reset password
# from django.utils.encoding import force_text
# from django.utils.http import urlsafe_base64_decode
# from .tokens import account_activation_token
# from django.views import View

from .forms import LoginForm, RegisterForm
from agenda.models import Agenda

User = get_user_model()


def register_view(request):
    # import ipdb
    # ipdb.set_trace()

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
            user.save()

        except Exception:  # this exception is too broad
            user = None
        """
        TO DO: add number of attempts here
        """
        if user is not None:
            # login(request, user)
            subject = "Welcome to Django Agenda"
            message = 'Here is a link to set your password'
            #message = render_to_string('account/email_content.html')
            recipient = email
            send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False)
            return redirect("/email_sent")
        else:
            request.session['register_error'] = 1  # 1 == True
            return render(request, "forms.html", {"form": form})

    return render(request, "forms.html", {"form": form})


# class ActivateAccountView(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#
#         if user is not None and account_activation_token.check_token(user, token):
#             user.save()
#             login(request, user)
#             return redirect('profile')
#         else:
#             # invalid link
#             return render(request, 'account/failure.html')


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

    return render(request, 'account/profile.html', {'agendas': agendas})


def logout_view(request):
    logout(request)  # request.user = Anon User
    return redirect("/login")
