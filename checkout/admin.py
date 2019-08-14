from django.contrib import admin

from checkout.models import Order, Ticket


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    fields = ('email', 'first_name', 'last_name', 'user')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInline,)
