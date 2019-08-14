from rest_framework import mixins
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from checkout.models import Order, Ticket
from checkout.serializers import OrderSerializer, TicketSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @permission_classes((IsAuthenticated,))
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(email=request.user.email)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TicketViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @permission_classes((IsAuthenticated,))
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(email=request.user.email)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
