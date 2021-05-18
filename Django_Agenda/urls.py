"""
Django_Agenda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path  # url

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


urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view),
    path('search/', search_view),
    path('agenda/', agenda_list_view),
    path('agenda/create/', agenda_create_view),
    path('agenda/<int:pk>/', agenda_detail_view),
    re_path(r'api/agenda/(?P<pk>\d+)/', agenda_api_detail_view),
    path('admin/', admin.site.urls),
]
