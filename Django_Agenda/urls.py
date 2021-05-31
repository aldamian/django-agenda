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
# from django.conf.urls import include
# from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts.views import (
    login_view,
    profile_view,
    logout_view,
    register_view,
    # ActivateAccountView,
)

from agenda.views import (
    search_view,
    agenda_create_view,
    agenda_detail_view,
    agenda_list_view,
    search_agenda_view,
    agenda_api_detail_view,
)
# pk - primary key

from django.views.generic import TemplateView

urlpatterns = [

    # path('', include('django.contrib.auth.urls')),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', agenda_list_view, name='home'),
    path('login/', login_view, name='login'),
    path('profile/<username>/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('email_sent/', TemplateView.as_view(template_name='account/email_sent.html'), name='email sent'),

    # url(r'^activate_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     ActivateAccountView.as_view(), name='activate_account'),

    # can't use this, changes the other views
    # path('account/', include('django.contrib.auth.urls')),


    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
         template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
         template_name='registration/password_change.html'),
         name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
         template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
         template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),


    path('agenda/', agenda_list_view, name='view agendas'),
    path('agenda/create/', agenda_create_view, name='create agenda'),
    path('agenda/<int:pk>/', agenda_detail_view),
    path('search/', search_view),
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
