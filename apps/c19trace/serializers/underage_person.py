from django.utils.translation import gettext_lazy as gettext
from rest_framework import serializers

from .. import models


class UnderagePerson(serializers.ModelSerializer):
    class Meta:
        model = models.UnderagePerson
        fields = (
            'name',
            'birth_date',
            'relationship',
            'gender'
        )
