from django.urls import path

from checkout.views import link_user_qtickets, webhook, user_tickets
from users.views import user_required

urlpatterns = [
    path('checkout/link/', link_user_qtickets, name='link_user_qtickets'),
    path('checkout/webhook/', webhook, name='qtickets_webhook'),
    path('me/tickets/', user_required(user_tickets), name='my_tickets'),
]
