from django.db import transaction
from rest_framework import serializers

from .. import models
from .place_check_point import PlaceCheckPoint


class Place(serializers.ModelSerializer):
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
            'place_type',
            'turistic_info_office_type',
            'rut',
            'service_type',
            'service_class',
            'name',
            'comuna',
            'localidad',
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