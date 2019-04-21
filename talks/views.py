from rest_framework import viewsets

from talks.models import Talk
from .serializers import TalkSerializer


class TalkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Talk.objects.all()
    serializer_class = TalkSerializer
