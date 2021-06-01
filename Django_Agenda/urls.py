"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/

Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from accounts.views import (
    login_view,
    profile_view,
    logout_view,
    register_view,
)

from agenda.views import (
    # search_view,
    agenda_create_view,
    agenda_detail_view,
    agenda_list_view,
    search_agenda_view,
    agenda_api_detail_view,
)
# pk - primary key

urlpatterns = [

    # path('', include('django.contrib.auth.urls')),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', agenda_list_view, name='home'),
    path('home/', TemplateView.as_view(template_name='home.html'), name='anon_home'),
    path('register/', register_view, name='register'),
    path('email_sent/', TemplateView.as_view(template_name='account/email_sent.html'), name='email sent'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<username>/', profile_view, name='profile'),


    # can't use this, changes the other views
    # path('account/', include('django.contrib.auth.urls')),

    path('password_change/', auth_views.PasswordChangeView.as_view(
         template_name='registration/password_change.html'),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
         template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
         template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    # path('set_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='set_password'),

    # User must be active and have usable password already
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
         template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),


    path('agenda/', agenda_list_view, name='view agendas'),
    path('agenda/create/', agenda_create_view, name='create agenda'),
    path('agenda/<int:pk>/', agenda_detail_view),
    # path('search/', search_view),
    path('search_agenda/', search_agenda_view, name='search by tags'),
    re_path(r'api/agenda/(?P<pk>\d+)/', agenda_api_detail_view),
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
