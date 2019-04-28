from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from checkout.models import Order, Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('email', 'first_name', 'last_name')


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'event', 'email', 'first_name', 'last_name', 'tickets')

    def validate_tickets(self, tickets):
        emails = {ticket['email'] for ticket in tickets}
        if len(emails) != len(tickets):
            raise ValidationError('Email`ы участников должны быть уникальны.')
        return tickets

    def create(self, validated_data):
        raw_tickets = validated_data.pop('tickets')
        order = Order.objects.create(**validated_data)
        tickets = [Ticket(**item, order=order) for item in raw_tickets]
        Ticket.objects.bulk_create(tickets)
        return order
