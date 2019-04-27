from django.urls import include, path
from rest_framework import routers

from checkout.views import OrderViewSet

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
