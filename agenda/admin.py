from django.contrib import admin

# Register your models here.
from .models import Agenda


class AgendaAdmin(admin.ModelAdmin):
    list_display = (
                    # 'user',  need to change user model to solve this error.
                    'title',
                    'entry_date',
                    'last_modified',
                    'tags',
                    'public',
                    'content',
                    'notify_me',
                    'notify_me_at'
                    )


admin.site.register(Agenda, AgendaAdmin)
