import qrcode
import qrcode.image.svg
from django.conf import settings
from django.db import transaction
from django.utils.translation import gettext_lazy as gettext
from fs_s3fs import S3FS
from rest_framework import serializers

from .underage_person import UnderagePerson
from .. import models


class Person(serializers.ModelSerializer):
    underage_persons = UnderagePerson(
        label=gettext('Underage persons'), many=True, allow_null=True, required=False
    )

    def create(self, validated_data):
        foreign_key_nesteds = ('underage_persons',)
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
                        value_item_serialized._validated_data['related_to_id'] = instance.id
                        value_item_serialized.save()

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=200,
                border=4,
            )
            qr.add_data(instance.id)
            qr.make(fit=True)

            #image = qrcode.make(qr, image_factory=qrcode.image.svg.SvgPathImage)
            image = qr.make_image()

            with S3FS(
                settings.MAIL_S3_BUCKET_NAME,
                aws_access_key_id=settings.MAIL_S3_BUCKET_AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.MAIL_S3_BUCKET_AWS_SECRET_ACCESS_KEY,
                acl="public-read"
            ) as s3:
                with s3.open(f'/qr/{instance.id}.png', 'wb+') as qr_image:
                    image.save(qr_image)

        return instance

    class Meta:
        model = models.Person
        fields = (
            'id',
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
            'underage_persons'
        )
