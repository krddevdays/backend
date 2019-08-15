from rest_framework import serializers

from checkout.models import Ticket


class UserTicketsSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(source='order.event_id')

    class Meta:
        model = Ticket
        fields = ('first_name', 'last_name', 'email', 'event_id')
        read_only_fields = ('first_name', 'last_name', 'email', 'event_id')
