from django.contrib import admin
from django.contrib.admin.widgets import AdminTextareaWidget
from django.utils.safestring import mark_safe

from .models import Event, Zone, Activity, Venue, Partner


class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 0
    fields = ('zone', 'type', 'thing_link', 'start_date', 'finish_date')
    readonly_fields = ('thing_link',)

    def get_queryset(self, request):
        return super(ActivityInline, self).get_queryset(request).order_by('start_date', 'zone')

    def thing_link(self, obj):
        return mark_safe(obj.thing.self_link())


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'venue')
    inlines = (ActivityInline,)
    fieldsets = (
        ('', {'fields': (('name', 'venue'), ('start_date', 'finish_date'), ('discussion_start', 'discussion_finish'))}),
        ('', {'fields': ('draft', 'published', 'canceled')}),
        ('Descriptions', {'fields': ('short_description', 'full_description', 'ticket_description')}),
        ('Images', {'fields': ('image', 'image_vk', 'image_facebook')}),
        ('Call for papers', {'fields': (('cfp_start', 'cfp_finish'), 'cfp_url')}),
        ('QTicket system', {'fields': ('external_id',)})
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in ('short_description', 'ticket_description'):
            kwargs['widget'] = AdminTextareaWidget
        return super(EventAdmin, self).formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'type', 'zone', 'start_date', 'finish_date')
    list_filter = ('event', 'zone', 'type')
    fieldsets = (
        ('', {'fields': (('event', 'zone', 'type'), ('start_date', 'finish_date'))}),
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


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'event', 'order')
    ordering = ('order',)
    list_filter = ('type', 'event')
