from django.urls import include, path

from checkout.views import link_user_qtickets

urlpatterns = [
    path('checkout/link', link_user_qtickets, name='link_user_qtickets'),
]
