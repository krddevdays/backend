from django.contrib import admin
from django.contrib.admin import BooleanFieldListFilter
from django.template.defaultfilters import safe
from django.urls import reverse

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
    readonly_fields = ('email', 'qticket_id', 'event', 'first_name', 'last_name',
                       'created_at', 'updated_at', 'payed_at', 'deleted_at', 'response')
    list_filter = ('event',)
    inlines = (TicketInline,)
    fieldsets = (
        (None, {
            'fields': (
                ('email', 'qticket_id', 'event'),
                ('first_name', 'last_name'),
                ('created_at', 'updated_at', 'payed_at', 'deleted_at'),
                ('response',)
            )}),)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'order_link', 'user_link', 'type', 'created_at', 'updated_at', 'deleted_at', 'get_payed_at')
    search_fields = ('qticket_id', 'email', 'first_name', 'last_name')
    readonly_fields = ('email', 'qticket_id', 'order', 'first_name', 'last_name',
                       'created_at', 'updated_at', 'deleted_at', 'pdf_url', 'passbook_url', 'type', 'price')
    list_filter = ('type', 'order__event', 'order__payed_at', ('user', BooleanFieldListFilter))
    fieldsets = (
        (None, {
            'fields': (
                ('user', 'qticket_id'),
                ('email', 'first_name', 'last_name'),
                ('created_at', 'updated_at', 'deleted_at'),
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
