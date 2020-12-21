from collections import OrderedDict
from copy import deepcopy

from django.db.models import OuterRef, Subquery, Count
from django.utils.translation import gettext_lazy as gettext
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from ... import serializers, models
from ...rest import permissions
from ...util.api import api_view
from ...util.datetime import start_day_date, start_week_date, start_month_date


class OwnProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method not in ["PUT", "PATCH", "DELETE"]
            or obj.owner
        )


class PlaceViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.PlaceInput
    queryset = models.Place.objects.all()
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.PlaceOutput
        else:
            return serializers.PlaceInput

    def get_queryset(self):
        queryset = super().get_queryset() \
            .filter(users__id=self.request.user.id) \
            .annotate(
                owner=Subquery(
                    models.PlaceUser
                    .objects
                    .filter(
                        user_id=self.request.user.id,
                        place_id=OuterRef('id')
                    )
                    .values('is_owner')
                )
            )

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
    permission_classes = [permissions.IsAuthenticated]


class TuristicServiceClassViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.TuristicServiceClass
    queryset = models.TuristicServiceClass.objects.filter(enabled=True)
    permission_classes = [permissions.IsAuthenticated]


@swagger_auto_schema(
    methods=["GET"],
    responses={200: serializers.PlaceUser(many=True)}
)
@swagger_auto_schema(
    methods=["POST"],
    responses={
        201: "Created",
        409: "Person already in this place"
    }
)
@api_view(http_method_names=["POST", "GET"], use_serializer=serializers.PlaceAddPerson)
@permission_classes((permissions.IsAuthenticated,))
def place_add_person(request: Request, id: int):
    if not models.PlaceUser.objects \
        .values_list('id', flat=True) \
        .filter(
            place_id=id, user_id=request.user.id,
            is_owner=True
        ) \
        .first() \
    :
        return Response(
            {"detail": gettext("You are not an owner of this place")},
            status=403
        )

    if request.method == "POST":
        if 'person_id' not in request.data:
            return Response(
                {"person_id": gettext('This field is required.')},
                status=400
            )

        try:
            person_id = request.data['person_id']
            is_owner = request.data.get('is_owner', False)
            user_id = models.Person.objects\
                .values_list('user_id', flat=True)\
                .get(id=person_id)
        except models.Person.DoesNotExist:
            return Response(
                {"non_field_errors": [gettext("Person with ID %s does not exists") % person_id]}
                , status=400
            )

        if not user_id:
            return Response(
                {"non_field_errors": [gettext("Person with ID %s does not have user") % person_id]}
                , status=400
            )

        current_place_user = models.PlaceUser.objects.only('id').filter(place_id=id, user_id=user_id).first()
        if current_place_user:
            return Response(
                {"non_field_errors": [gettext("Person with ID %s is already in this place") % person_id]}
                , status=409
            )

        models.PlaceUser(
            place_id=id, user_id=user_id, is_owner=is_owner
        )\
            .save()

        return Response(status=201)
    else:  # GET
        return Response(
            tuple(map(
                lambda row: {
                    'id': row['user__person__id'],
                    'full_name': "%s %s" % (
                        row['user__person__names'],
                        row['user__person__first_surname']
                    ),
                    'is_owner': row['is_owner']
                },
                models.PlaceUser
                    .objects
                    .filter(place_id=id)
                    .values(
                        'user__person__id', 'user__person__names',
                        'user__person__first_surname', 'is_owner'
                    )
            ))
        )


@swagger_auto_schema(
    methods=["DELETE"],
    responses={204: "When deleted"}
)
@api_view(http_method_names=["DELETE"], use_serializer=serializers.PlaceAddPerson)
@permission_classes((permissions.IsAuthenticated,))
def place_delete_person(request: Request, id: int, person_id):
    if not models.PlaceUser.objects \
        .values_list('id', flat=True) \
        .filter(
            place_id=id, user_id=request.user.id,
            is_owner=True
        ) \
        .first() \
    :
        return Response(
            {"detail": gettext("You are not an owner of this place")},
            status=403
        )

    place_person = get_object_or_404(
        models.PlaceUser,
        user__person__id=person_id,
        place_id=id
    )

    place_person.delete()
    return Response(status=204)


@api_view(http_method_names=["GET"], use_serializer=serializers.Stats)
@permission_classes((permissions.IsAuthenticated,))
def stats(request, id):
    if not models.PlaceUser.objects \
        .values_list('id', flat=True) \
        .filter(
            place_id=id, user_id=request.user.id,
            is_owner=True
        ) \
        .first() \
    :
        return Response(
            {"detail": gettext("You are not an owner of this place")},
            status=403
        )

    timezone = "America/Santiago"
    stats_groups = ('today', 'week', 'month')
    base_query = models.PlacePersonCheck\
        .objects\
        .annotate(ids=Count('id')) \
        .values('ids') \
        .filter(place_id=id)

    stats = models.Place.objects\
        .annotate(
            today=deepcopy(base_query).filter(creation_date__gte=start_day_date(timezone)),
            week=deepcopy(base_query).filter(creation_date__gte=start_week_date(timezone)),
            month=deepcopy(base_query).filter(creation_date__gte=start_month_date(timezone))
        )\
        .values_list(*stats_groups)\
        [0:1][0]

    return Response(
        OrderedDict(zip(
            stats_groups,
            (
                0 if stat is None else stat
                for stat in stats
            )
        ))
    )
