from rest_framework import serializers

from .. import models


class EntryPoint(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(label="ID")

    class Meta:
        model = models.EntryPoint
        fields = ('id', 'name', 'type')
