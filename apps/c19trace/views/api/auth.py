from datetime import datetime

import pytz
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class TokenObtainPairCustomSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data.update({
            'lifetime': int(refresh.access_token.lifetime.total_seconds()),
            'expires': datetime.utcnow().replace(tzinfo=pytz.utc).isoformat(),
            'person_id': self.user.person.id,
            'names': self.user.person.names
        })

        return data


class TokenObtainPairCustomView(TokenObtainPairView):
    serializer_class = TokenObtainPairCustomSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


class TokenRefreshPairCustomSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        data.update({
            'lifetime': int(refresh.access_token.lifetime.total_seconds()),
            'expires': datetime.utcnow().replace(tzinfo=pytz.utc).isoformat(),
        })
        return data


class TokenRefreshPairCustomView(TokenObtainPairView):
    serializer_class = TokenRefreshPairCustomSerializer
    token_obtain_pair = TokenObtainPairView.as_view()