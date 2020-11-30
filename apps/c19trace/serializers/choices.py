from django.utils.translation import gettext_lazy as gettext
from rest_framework import serializers


class CharChoices(serializers.Serializer):
    value = serializers.CharField(
        label=gettext("Value"), max_length=64
    )
    label = serializers.CharField(
        label=gettext("Label"), max_length=64
    )


class IntegerChoices(serializers.Serializer):
    value = serializers.IntegerField(
        label=gettext("Value")
    )
    label = serializers.CharField(
        label=gettext("Label"), max_length=64
    )
