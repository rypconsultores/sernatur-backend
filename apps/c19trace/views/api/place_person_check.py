from collections.abc import Mapping as MappingBase
from typing import Any, Sequence, Mapping, List, Dict

from django.http import Http404
from django.utils.translation import gettext_lazy as gettext
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Empty, Request
from rest_framework.response import Response

from ... import models, serializers
from ...util.api import api_view


@swagger_auto_schema(
    methods=["PUT"],
    responses={
        200: serializers.PlacePersonCheckOutput(help_text=gettext("When Update")),
        201: serializers.PlacePersonCheckOutput(help_text=gettext("When Create")),
    }
)
@api_view(['PUT'], serializers.PlacePersonCheckSwagger)
@permission_classes([IsAuthenticated])
def check_upsert(request, place_id, person_id):
    place_person_check = models.PlacePersonCheck\
        .objects\
        .filter(place_id=place_id, person=person_id) \
        .first()

    serializer_kwargs = dict(data=request.data)
    if hasattr(request.data, '_mutable'):
        request.data._mutable = True

    request.data['place_id'] = place_id
    request.data['person_id'] = person_id

    if place_person_check:
        serializer_kwargs['instance'] = place_person_check

    place_person_check_serializer = serializers\
        .PlacePersonCheckInput(**serializer_kwargs)

    place_person_check_serializer.is_valid(True)
    place_person_check_serializer.save()

    return Response(
        serializers.PlacePersonCheckOutput(
            instance=place_person_check_serializer.instance
        ).data,
        200 if place_person_check else 201
    )


@api_view(['GET'], serializers.PlacePersonCheckOutput)
@permission_classes([IsAuthenticated])
def check_retrieve(request, place_id, person_id, check_id):
    place_person_check = get_object_or_404(
        models.PlacePersonCheck,
        place_id=place_id, person=person_id, id=check_id
    )

    return Response(
        serializers.PlacePersonCheckOutput(
            instance=place_person_check
        ).data
    )


@swagger_auto_schema(
    methods=["GET"],
    responses={
        200: serializers.PlaceOutput(many=True)
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def by_person(request, user_id):
    if not (
        request.user.is_superuser
        or request.user.user_extra_conf.traceability
    ):
        raise Response(
            {"message": "You don't have permission to access"}, 403
        )

    user_id = models.User.objects\
        .values_list('id', flat=True)\
        .filter(id=user_id)\
        .first()

    if not user_id:
        raise Http404()

    return Response(
        serializers.Place(
            models.Place.objects.filter(persons_checks__user_id=user_id),
            many=True
        )
    )

