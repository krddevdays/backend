from django.urls import path, include
from rest_framework import routers

from users.views import login, logout, registration, UserView, user_required, CompanyViewSet

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)


urlpatterns = [
    path('me/', user_required(UserView.as_view()), name='me'),
    path('registration/', registration, name='registration'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('', include(router.urls)),
]
