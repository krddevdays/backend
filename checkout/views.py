from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from checkout.models import Order
from checkout.serializers import OrderSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
