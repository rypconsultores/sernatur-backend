from django.db import transaction
from django.utils.translation import gettext_lazy as gettext
from rest_framework import serializers

from .person import Person
from .place import PlaceOutput
from .. import models


class PlacePersonCheckSymptoms(serializers.ModelSerializer):
    class Meta:
        model = models.PlacePersonCheckSymptom
        exclude = ('id',)


class PlacePersonCheckInput(serializers.ModelSerializer):
    person_id = serializers.CharField(
        help_text=gettext("It fills automatically from path"),
        label=gettext("Person ID"),
        max_length=models.Person._meta.get_field('id').max_length
    )
    place_id = serializers.IntegerField(
        help_text=gettext("It fills automatically from path"),
        label=gettext("Place ID")
    )
    symptoms = PlacePersonCheckSymptoms()
    place_check_point_id = serializers.IntegerField(
        label=gettext("Place check point ID")
    )

    def save(self):
        with transaction.atomic():
            if self.initial_data['symptoms']:
                symptoms = PlacePersonCheckSymptoms(
                    data=self._validated_data['symptoms']
                )
                symptoms.is_valid()
                self._validated_data['symptoms'] = symptoms.save()

            instance = super().save()

        return instance

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


class PlacePersonCheckSwagger(serializers.ModelSerializer):
    symptoms = PlacePersonCheckSymptoms()
    place_check_point_id = serializers.IntegerField(
        label=gettext("Place check point ID")
    )

    class Meta:
        model = models.PlacePersonCheck
        fields = (
            'id', 'symptoms', 'creation_date',
            'modification_date', 'observations',
            'place_check_point_id'
        )
        extra_kwargs = {
            "creation_date": {"read_only": True},
            "modification_date": {"read_only": True},
        }


class PlacePersonCheckOutput(serializers.ModelSerializer):
    person = Person()
    place = PlaceOutput()
    symptoms = PlacePersonCheckSymptoms()
    place_check_point_id = serializers.IntegerField(
        label=gettext("Place check point ID")
    )

    class Meta:
        model = models.PlacePersonCheck
        fields = (
            'id', 'symptoms', 'creation_date',
            'modification_date', 'observations',
            'place', 'place_check_point_id',
            'person'
        )
        extra_kwargs = {
            "creation_date": {"read_only": True},
            "modification_date": {"read_only": True},
        }
