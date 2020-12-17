from django.utils.translation import gettext_lazy as gettext
from rest_framework import serializers
from rest_framework_gis import serializers as serializers_gis

from .. import models


class PlacePersonCheckSymptoms(serializers.ModelSerializer):
    class Meta:
        model = models.PlacePersonCheckSymptom
        exclude = ('id',)


class PlacePersonCheck(serializers.ModelSerializer):
    symptoms = PlacePersonCheckSymptoms()
    place_id = serializers.IntegerField(
        help_text=gettext("It fills automatically from path"),
        label=gettext("Place ID")
    )
    place_check_point_id = serializers.IntegerField(
        label=gettext("Place check point ID")
    )
    person_id = serializers.CharField(
        label=gettext("Person ID"),
        max_length=models.Person._meta.get_field('id').max_length
    )

    class Meta:
        model = models.PlacePersonCheck
        fields = (
            'id', 'symptoms', 'creation_date',
            'modification_date', 'observations',
            'place_id', 'place_check_point_id',
            'person_id'
        )
        extra_kwargs = {
            "creation_date": {"read_only": True},
            "modification_date": {"read_only": True},
        }
