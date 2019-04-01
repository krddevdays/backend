from django.contrib import admin

from .models import Event, Place, Activity, Location


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'location')
    inlines = (ActivityInline,)
    fieldsets = (
        ('', {'fields': (('name', 'location'),)}),
        ('', {'fields': (('start_date', 'finish_date'),)})
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('event', 'type', 'name', 'place', 'start_date', 'finish_date')
    list_filter = ('event', 'place')


class PlacesInline(admin.TabularInline):
    model = Place
    extra = 0


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    inlines = (PlacesInline,)
