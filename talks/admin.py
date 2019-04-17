from django.contrib import admin

from talks.models import Speaker, Talk


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {'fields': (('first_name', 'last_name'), ('work', 'position'))}),
    )


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    pass
