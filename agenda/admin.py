from django.contrib import admin

# Register your models here.
from .models import Agenda


# class AgendaAdmin(admin.ModelAdmin):
#     list_display = (
#                     'user',
#                     'title',
#                     'entry_date',
#                     'last_modified',
#                     'tags',
#                     'agenda_visibility',
#                     'content',
#                     'notify_me',
#                     'notify_me_at'
#                     )


admin.site.register(Agenda)
