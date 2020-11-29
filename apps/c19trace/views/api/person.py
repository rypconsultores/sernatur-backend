from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet

from ... import serializers, models


class PersonViewSet(
    mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.Person
    queryset = models.Person.objects.all()
