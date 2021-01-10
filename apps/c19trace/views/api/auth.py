from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from ...serializers import auth as serializers


class TokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.TokenObtainPair
    token_obtain_pair = TokenObtainPairView.as_view()

    @swagger_auto_schema(
        responses={
            200: serializers.TokenOutput
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshPairView(TokenObtainPairView):
    serializer_class = serializers.TokenRefreshPair
    token_obtain_pair = TokenObtainPairView.as_view()

    @swagger_auto_schema(
        responses={
            200: serializers.TokenOutput
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenDestroyPairView(TokenObtainPairView):
    serializer_class = serializers.TokenDestroyPair
    token_obtain_pair = TokenObtainPairView.as_view()

    @swagger_auto_schema(
        responses={
            204: 'When successfully delete'
        }
    )
    def post(self, request, *args):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)