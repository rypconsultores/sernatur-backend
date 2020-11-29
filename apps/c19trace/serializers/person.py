from rest_framework.serializers import ModelSerializer

from .. import models


class Person(ModelSerializer):
    class Meta:
        model = models.Person
        fields = (
            'date',
            'first_surname',
            'last_surname',
            'names',
            'gender',
            'birth_date',
            'nationality',
            'travel_document',
            'document_no',
            'residence',
            'residence_chile_region',
            'residence_chile_comuna',
            'residence_other_country',
            'residence_other_place',
            'email',
            'mobile_phone',
            'visit_subject',
            'visit_no',
            'transportation_mode',
            'destination',
            'entry_point',
            'main_transportation_mean',
            'contact_name',
            'contact_relationship',
            'contact_phone_or_email',
            'contact_comuna',
            'contact_localidad',
        )
