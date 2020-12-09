from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ... import serializers, models


class PlaceViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.Place
    queryset = models.Place.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users__id=self.request.user.id)
        print(str(queryset.query))
        return queryset

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        models.PlaceUser(
            user=request.user, place=serializer.instance, is_owner=1
        ).save()

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TuristicServiceTypeViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.TuristicServiceType
    queryset = models.TuristicServiceType.objects.filter(enabled=True)
    permission_classes = [IsAuthenticated]


class TuristicServiceClassViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.TuristicServiceClass
    queryset = models.TuristicServiceClass.objects.filter(enabled=True)
    permission_classes = [IsAuthenticated]
