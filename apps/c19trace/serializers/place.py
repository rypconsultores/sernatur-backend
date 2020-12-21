

from django.db import transaction
from django.utils.translation import gettext_lazy as gettext
from rest_framework import serializers

from .. import models
from .place_check_point import PlaceCheckPoint


class PlaceInput(serializers.ModelSerializer):
    owner = serializers.BooleanField(
        label=gettext('Owner'), read_only=True
    )
    check_points = PlaceCheckPoint(
        label=models.PlaceCheckPoint._meta.verbose_name_plural, many=True
    )

    def create(self, validated_data):
        foreign_key_nesteds = ('check_points',)
        list_values = {}

        with transaction.atomic():
            for field in foreign_key_nesteds:
                if field in validated_data:
                    list_values[field] = validated_data.pop(field)

            instance = super().create(validated_data)

            for field in foreign_key_nesteds:
                field_serializer = self.fields[field]

                if field in list_values:
                    for value_item in list_values[field]:
                        value_item_serialized: serializers.ModelSerializer = \
                            field_serializer.child.__class__(data=value_item)
                        value_item_serialized.is_valid(raise_exception=True)
                        value_item_serialized._validated_data['place_id'] = instance.id
                        value_item_serialized.save()

        return instance

    class Meta:
        model = models.Place
        fields = (
            'id',
            'place_type',
            'turistic_info_office_type',
            'rut',
            'service_type',
            'service_class',
            'name',
            'comuna',
            'localidad',
            'owner',
            'zone',
            'address',
            'representative_name',
            'representative_position',
            'representative_phone',
            'representative_mail',
            'check_points'
        )


class TuristicServiceType(serializers.ModelSerializer):
    class Meta:
        model = models.TuristicServiceType
        fields = (
            'id', 'name'
        )


class TuristicServiceClass(serializers.ModelSerializer):
    class Meta:
        model = models.TuristicServiceClass
        fields = (
            'id', 'name', 'type'
        )


class PlaceAddPerson(serializers.Serializer):
    person_id = serializers.CharField(
        min_length=models.Person._meta.get_field('id').max_length,
        max_length=models.Person._meta.get_field('id').max_length,
        label=models.Person._meta.verbose_name,
    )


class PlaceUser(PlaceAddPerson):
    full_name = serializers.CharField(
        label=gettext("Full name")
    )
    is_owner = serializers.BooleanField(
        label=models.PlaceUser._meta.get_field('is_owner').verbose_name
    )


class PlaceType(serializers.Serializer):
    id = serializers.IntegerField(
        label=gettext("ID")
    )

    name = serializers.CharField(
        label=gettext("Name")
    )

    def to_internal_value(self, data):
        return self.id

    def to_representation(self, type_id):
        return {
            "id": type_id,
            "name": next((
                o[1]
                for o in models.Place._place_type_choices
                if o[0] == type_id
            ))
        }


class PlaceOutput(serializers.ModelSerializer):
    place_type = PlaceType(
        label="PlaceType",
        help_text=models.Place._meta.get_field('place_type').verbose_name
    )
    service_type = TuristicServiceType(
        label='TuristicServiceType',
        help_text=models.TuristicServiceType._meta.verbose_name
    )
    service_class = TuristicServiceClass(
        label='TuristicServiceClass',
        help_text=models.TuristicServiceClass._meta.verbose_name
    )
    owner = serializers.BooleanField(
        label=gettext('Owner'), read_only=True
    )
    check_points = PlaceCheckPoint(
        label=models.PlaceCheckPoint._meta.verbose_name_plural, many=True
    )

    class Meta(PlaceInput.Meta):
        pass


class Stats(serializers.Serializer):
    today = serializers.IntegerField(
        label=gettext("Today person checks count in the current place")
    )
    week = serializers.IntegerField(
        label=gettext("Person checks count of the week in the current place")
    )
    month = serializers.IntegerField(
        label=gettext("Person checks count of the month in the current place")
    )