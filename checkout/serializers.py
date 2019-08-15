from rest_framework import serializers

from checkout.models import Ticket


class UserTicketsSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(source='order.event_id')
    payed_at = serializers.DateTimeField(source='order.payed_at')
    number = serializers.IntegerField(source='qticket_id')

    class Meta:
        model = Ticket
        fields = ('first_name', 'last_name', 'email', 'event_id', 'created_at', 'updated_at', 'deleted_at', 'payed_at', 'pdf_url', 'passbook_url', 'type', 'number', 'price')
        read_only_fields = ('first_name', 'last_name', 'email', 'event_id')
