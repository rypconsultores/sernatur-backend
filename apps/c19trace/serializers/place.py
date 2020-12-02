from rest_framework.serializers import ModelSerializer

from .. import models


class Place(ModelSerializer):
    class Meta:
        model = models.Place
        fields = (
            'place_type',
            'turistic_info_office_type',
            'rut',
            'service_type',
            'name',
            'comuna',
            'localidad',
            'zone',
            'address',
            'representative_name',
            'representative_position',
            'representative_phone',
            'representative_mail',
        )
