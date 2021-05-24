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
from django.urls import path, re_path, include
from django.conf.urls.static import static
# from django.contrib.auth import views as auth_views

from accounts.views import (
    login_view,
    logout_view,
    register_view,
)

from agenda.views import (
    search_view,
    agenda_create_view,
    agenda_detail_view,
    agenda_list_view,
    agenda_api_detail_view,
)
# pk - primary key

from django.views.generic import TemplateView

urlpatterns = [

    path('', TemplateView.as_view(template_name='home.html')),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view),
    path('email_sent/', TemplateView.as_view(template_name='account/email_sent.html')),

    # path('password-reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'),
    #      name='password_reset'),
    # path('password-reset-confirm/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),
    #      name='password_reset_confirm'),

    path('search/', search_view),
    path('agenda/', agenda_list_view),
    path('agenda/create/', agenda_create_view),
    path('agenda/<int:pk>/', agenda_detail_view),
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
