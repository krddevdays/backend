from django.urls import include, path
from rest_framework import routers

from checkout.views import OrderViewSet, TicketViewSet

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'tickets', TicketViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
