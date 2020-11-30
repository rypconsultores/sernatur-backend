from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet

from ... import serializers, models


class EntryPointViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.EntryPoint
    queryset = models.EntryPoint.objects.all()
