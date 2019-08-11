from django.urls import path

from users.views import login, logout, registration, UserView, user_required

urlpatterns = [
    path('me/', user_required(UserView.as_view()), name='me'),
    path('registration/', registration, name='registration'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
