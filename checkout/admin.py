import csv

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from django.template.defaultfilters import safe
from django.urls import reverse

from checkout.filters import NotNullBooleanFieldListFilter
from checkout.models import Order, Ticket


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    fields = ('email', 'first_name', 'last_name', 'qticket_id', 'user')
    readonly_fields = ('email', 'first_name', 'last_name', 'qticket_id')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'event', 'created_at', 'updated_at', 'deleted_at', 'payed_at')
    search_fields = ('qticket_id', 'email', 'first_name', 'last_name')
    readonly_fields = ('email', 'qticket_id', 'event', 'first_name', 'last_name', 'response', 'client_phone',
                       'created_at', 'updated_at', 'payed_at', 'deleted_at', 'reserved_to', 'reserved')
    list_filter = ('event',)
    inlines = (TicketInline,)
    fieldsets = (
        (None, {
            'fields': (
                ('email', 'qticket_id', 'event'),
                ('first_name', 'last_name', 'client_phone'),
                ('created_at', 'updated_at', 'payed_at', 'deleted_at', 'reserved_to', 'reserved'),
                ('response',)
            )}),)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'order_link', 'user_link', 'type', 'created_at',
                    'updated_at', 'deleted_at', 'get_payed_at')
    search_fields = ('qticket_id', 'email', 'first_name', 'last_name')
    readonly_fields = ('email', 'qticket_id', 'order', 'first_name', 'last_name', 'client_phone', 'refunded_at',
                       'created_at', 'updated_at', 'deleted_at', 'pdf_url', 'passbook_url', 'type', 'price')
    list_filter = ('type', 'order__event', 'order__payed_at', 'deleted_at', 'refunded_at',
                   ('user', NotNullBooleanFieldListFilter))
    fieldsets = (
        (None, {
            'fields': (
                ('user', 'qticket_id'),
                ('email', 'first_name', 'last_name', 'client_phone'),
                ('created_at', 'updated_at', 'deleted_at', 'refunded_at'),
            )}),
        (None, {'fields': (('pdf_url', 'passbook_url'), ('type', 'price'))})
    )

    def order_link(self, obj: Ticket):
        link = reverse('admin:checkout_order_change', args=(obj.order_id,))
        return safe(f'<a href="{link}">{obj.order}</a>')

    def user_link(self, obj: Ticket):
        if obj.user is None:
            return '-'
        link = reverse('admin:users_user_change', args=(obj.user_id,))
        return safe(f'<a href="{link}">{obj.user}</a>')

    def get_payed_at(self, obj: Ticket):
        return obj.order.payed_at

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def export(self, request):
        cl = self.get_changelist_instance(request)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tickets.csv"'
        writer = csv.writer(response, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        keys = ['email'] + list(Ticket.qticket_fields.keys())
        writer.writerow(keys)
        for item in cl.queryset.all():
            writer.writerow([getattr(item, field) for field in keys])
        return response

    def get_urls(self):
        urls = super(TicketAdmin, self).get_urls()
        model_info = (self.model._meta.app_label, self.model._meta.model_name)
        employer_urls = [
            url(r'^export/$', self.admin_site.admin_view(self.export), name='%s_%s_export' % model_info),
        ]
        return employer_urls + urls
