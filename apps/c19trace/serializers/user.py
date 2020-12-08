from django.contrib.auth.models import User
from rest_framework import serializers

from .. import models


class PasswordChangeOrCreateRequest(serializers.Serializer):
    email = serializers.CharField(
        label=models.Person._meta.get_field('email').verbose_name,
        max_length=models.Person._meta.get_field('email').max_length
    )
    document_no = serializers.CharField(
        label=models.Person._meta.get_field('document_no').verbose_name
    )


class PasswordChangeOrCreate(serializers.ModelSerializer):
    class Meta:
        model = models.PasswordChangeOrCreate
        fields = ('id', 'key')


class PasswordSet(serializers.Serializer):
    key = serializers.CharField(
        label=models.PasswordChangeOrCreate._meta.get_field('key').verbose_name,
        max_length=models.PasswordChangeOrCreate._meta.get_field('key').max_length
    )
    password = serializers.CharField(
        label=User._meta.get_field('password').verbose_name
    )