from django.contrib import admin

from checkout.models import Order, Ticket


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    fields = ('email', 'full_name', 'form')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInline,)
