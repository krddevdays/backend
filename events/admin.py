from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from requests import HTTPError

from .models import Event, Zone, Activity, Venue
from .utils import ExternalSystemError, check_qtickets_event


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 0
    fields = ('zone', 'type', 'thing_link', 'start_date', 'finish_date')
    readonly_fields = ('thing_link',)

    def get_queryset(self, request):
        return super(ActivityInline, self).get_queryset(request).order_by('start_date', 'zone')

    def thing_link(self, obj):
        return mark_safe(obj.thing.self_link())


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def clean_external_id(self):
        data = self.cleaned_data['external_id']
        try:
            check_qtickets_event(data)
        except ExternalSystemError as e:
            raise forms.ValidationError(e)
        except HTTPError as e:
            raise forms.ValidationError(e)
        return data


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'venue')
    inlines = (ActivityInline,)
    form = EventForm
    fieldsets = (
        ('', {'fields': (('name', 'venue'),)}),
        ('', {'fields': (('start_date', 'finish_date'),)}),
        ('QTicket system', {'fields': ('external_id',)})
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'type', 'zone', 'start_date', 'finish_date')
    list_filter = ('event', 'zone', 'type')
    fieldsets = (
        ('', {'fields': (('event', 'zone', 'type'), 'thing', ('start_date', 'finish_date'))}),
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
