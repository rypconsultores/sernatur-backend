from django.utils.translation import gettext_lazy as gettext
from rest_framework import serializers
from rest_framework_gis import serializers as serializers_gis

from .. import models


class PointField(serializers_gis.GeometryField, serializers.Serializer):
    type = serializers.ChoiceField(
        label=gettext("Geometry type"), choices=(("Point", "Point"),)
    )
    coordinates = serializers.ListField(
        child=serializers.FloatField(),
        label="Coordinates",
        max_length=2, min_length=2, required=True
    )


class PlaceCheckPoint(serializers.ModelSerializer):
    location = PointField(
        label=gettext("Location")
    )

    class Meta:
        model = models.PlaceCheckPoint
        fields = ('name', 'location', 'id')
