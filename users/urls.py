from django.urls import path, include
from rest_framework import routers

from users.views import login, logout, registration, UserView, user_required, reset_password, set_password, CompanyViewSet

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)

reset_password_patterns = [
    path('', reset_password, name='reset_password'),
    path('set/', set_password, name='set_password'),
]

urlpatterns = [
    path('me/', user_required(UserView.as_view()), name='me'),
    path('registration/', registration, name='registration'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('', include(router.urls)),
    path('reset_password/', include(reset_password_patterns)),
]
