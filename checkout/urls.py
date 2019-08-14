from django.urls import include, path

from checkout.views import link_user_qtickets, webhook

urlpatterns = [
    path('checkout/link/', link_user_qtickets, name='link_user_qtickets'),
    path('checkout/webhook/', webhook, name='qtickets_webhook'),
]
