from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('events.urls')),
    path('', include('talks.urls')),
    path('docs/', include_docs_urls(title='Krasnodar Dev Days API'))
    path('', include('checkout.urls')),
]
