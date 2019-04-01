from django.contrib import admin

from .models import Event, Place, Activity, Location


class ActivityInline(admin.TabularInline):
    model = Activity


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'location')
    inlines = (ActivityInline,)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    list_filter = ('location',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('event', 'type', 'name', 'place', 'start_date', 'finish_date')
    list_filter = ('event', 'place')


class PlacesInline(admin.TabularInline):
    model = Place
    extra = 1


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    list_filter = ('place',)
    inlines = (PlacesInline,)
