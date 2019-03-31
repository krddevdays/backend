from django.contrib import admin

from events.models import Event, Area, Activity


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    pass


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass
