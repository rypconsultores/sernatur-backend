from datetime import datetime

import pytz
from django.utils.translation import gettext_lazy as gettext
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class TokenOutput(serializers.Serializer):
    refresh = serializers.CharField(label=gettext("Refresh token"))
    access = serializers.CharField(label=gettext("Access token"))
    lifetime = serializers.IntegerField(label=gettext("Life time (seconds)"), min_value=0)
    expires = serializers.DateTimeField(label=gettext('Expiration date/time'))


class TokenObtainPair(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data.update({
            'lifetime': int(refresh.access_token.lifetime.total_seconds()),
            'expires': datetime.utcnow().replace(tzinfo=pytz.utc).isoformat(),
        })

        return data


class TokenRefreshPair(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        data.update({
            'lifetime': int(refresh.access_token.lifetime.total_seconds()),
            'expires': datetime.utcnow().replace(tzinfo=pytz.utc).isoformat(),
            'person_id': self.user.person.id,
            'names': self.user.person.names
        })
        return data


class TokenDestroyPair(TokenRefreshPair):
    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self.token = None

    default_error_messages = {
        'bad_token': gettext('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
