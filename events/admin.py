from django.contrib import admin

from .models import Event, Zone, Activity, Venue


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 0
    fields = ('zone', 'type', 'related_thing', 'start_date', 'finish_date')
    readonly_fields = ('related_thing',)

    def get_queryset(self, request):
        return super(ActivityInline, self).get_queryset(request).order_by('start_date', 'zone')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'venue')
    inlines = (ActivityInline,)
    fieldsets = (
        ('', {'fields': (('name', 'venue'),)}),
        ('', {'fields': (('start_date', 'finish_date'),)})
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'type', 'zone', 'start_date', 'finish_date')
    list_filter = ('event', 'zone', 'type')
    fieldsets = (
        ('', {'fields': (('event', 'zone', 'type'), 'related_thing', ('start_date', 'finish_date'))}),
    )

    def get_queryset(self, request):
        return super(ActivityAdmin, self).get_queryset(request).order_by('start_date', 'zone')


class ZonesInline(admin.TabularInline):
    model = Zone
    extra = 0


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'latitude', 'longitude')
    inlines = (ZonesInline,)
    fieldsets = (
        ('', {'fields': (('name', 'address'), ('latitude', 'longitude'))}),
    )
