from django.contrib import admin

from talks.models import Speaker, Talk, Discussion


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {'fields': (('first_name', 'last_name'), 'avatar', ('work', 'position'))}),
    )


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    pass


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    save_as = True
    pass
