from copy import deepcopy

import django_filters.rest_framework as filters
from csv_export.views import CSVExportView
from django.db.models import Q
from django.http import Http404
from django.utils.dateparse import parse_datetime
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as gettext
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets, pagination
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from ... import models, serializers
from ...rest import permissions
from ...util.api import api_view


@swagger_auto_schema(
    methods=["PUT"],
    responses={
        200: serializers.PlacePersonCheckOutput(help_text=gettext("When Update")),
        201: serializers.PlacePersonCheckOutput(help_text=gettext("When Create")),
    }
)
@api_view(['PUT'], serializers.PlacePersonCheckSwagger)
@permission_classes([permissions.IsAuthenticated])
def check_upsert(request, place_id, person_id):
    if 'id' not in request.data:
        return Response(
            {"id": gettext("This field is required")}, status=400
        )

    place_person_check = models.PlacePersonCheck\
        .objects\
        .filter(
            place_id=place_id, person=person_id,
            id=request.data['id']
        ) \
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
@permission_classes([permissions.IsAuthenticated])
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
@permission_classes([permissions.IsSuperuserOrTracerUser])
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


class PlacePersonCheckViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.PlacePersonCheckOutput
    queryset = models.PlacePersonCheck.objects.all()
    permission_classes = [permissions.IsSuperuserOrTracerUser]


class PlacePersonCheckBaseFiltersetMixin():
    date__range = filters.CharFilter(
        method="date_range",
        help_text=gettext('Format: `<ISO DateTime>,<ISO DateTime>`')
    )

    @staticmethod
    def date_range(queryset, name, value):
        date_range = value.split(',')

        if len(date_range) != 2:
            error = [gettext('Invalid format, format is `<ISO DateTime>,<ISO DateTime>`.')]
        else:
            error = []
            date_range = [parse_datetime(date) for date in date_range]
            for idx, error_str in enumerate((
                    gettext("Invalid `from` date (first one)"),
                    gettext("Invalid `to` date (second one)"),
            )):
                if not date_range[idx]:
                    error.append(error_str)

        if error:
            raise APIException(
                detail={"date__range": error}, code=400
            )

        return queryset.filter(
            Q(creation_date__range=date_range)
            | Q(modification_date__range=date_range)
        )

    symptoms = filters.CharFilter(
        method="symptoms_filter",
        help_text=gettext(
            f"""A comma separated symptoms using the following values:
- `cough`: Cough
- `dispnea`: Dispnea or breathing difficulty
- `thoracic_pain`: Throracic pain
- `throat_pain`: Throat pain or odynophagia
- `muscular_articular_pain`: Myalgia, muscular or articular pain
- `chills`: Chills
- `headache`: Headache
- `diarrhea`: Diarrhea
- `lost_smell`: Abrupt lost of smell
- `lost_taste`: Abrupt lost of taste
- `fever`: Fever
            """
        )
    )


    def symptoms_filter(self, queryset, name, value):
        symptoms_list = (
            'cough',
            'dispnea',
            'thoracic_pain',
            'throat_pain',
            'muscular_articular_pain',
            'chills',
            'headache',
            'diarrhea',
            'lost_smell',
            'lost_taste',
            'fever',
        )

        filter = None
        errors = []
        symptoms = value.split(',')
        for symptom in symptoms:
            if symptom not in symptoms_list:
                errors.append(gettext("Symptom `%s` does not exists.") % (symptom,))
                continue

            q_value = Q(**{(self.symptoms_base_query + symptom): True})
            if filter is None:
                filter = q_value
            else:
                filter |= q_value

        if errors:
            raise APIException(
                detail={"symptoms": errors}, code=400
            )

        if filter:
            return queryset.filter(filter)
        else:
            return queryset


class PlacePersonCheckByUserFilterset(
    PlacePersonCheckBaseFiltersetMixin, filters.FilterSet
):
    date__range = deepcopy(PlacePersonCheckBaseFiltersetMixin.date__range)
    symptoms = deepcopy(PlacePersonCheckBaseFiltersetMixin.symptoms)
    symptoms_base_query = 'symptoms__'


class PlacePersonCheckViewSetByUser(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.PlacePersonCheckOutput
    queryset = models.PlacePersonCheck.objects.all()
    permission_classes = [permissions.IsSuperuserOrTracerUser]
    lookup_field = 'user_id'
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PlacePersonCheckByUserFilterset


class PlacePersonCheckByPlaceFilterset(
    PlacePersonCheckBaseFiltersetMixin, filters.FilterSet
):
    date__range = deepcopy(PlacePersonCheckBaseFiltersetMixin.date__range)
    symptoms = deepcopy(PlacePersonCheckBaseFiltersetMixin.symptoms)
    symptoms_base_query = 'symptoms__'

    class Meta:
        model = models.PlacePersonCheck
        fields = ('place_check_point_id',)


class PlacePersonCheckViewSetByPlace(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.PlacePersonCheckOutput
    queryset = models.PlacePersonCheck.objects.all()
    permission_classes = [permissions.IsSuperuserOrTracerUser]
    lookup_field = 'place_id'
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PlacePersonCheckByPlaceFilterset


class PlacePersonCheckByPlaceExportView(CSVExportView):
    http_method_names = ["get"]
    model = models.PlacePersonCheck
    fields = (
        'creation_date','place__name','place_check_point__name','person__names',
        'person__first_surname', 'person__last_surname', 'person__nationality',
        'person__travel_document', 'person__document_no', 'person__email',
        'person__mobile_phone'
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(place_id=self.kwargs['place_id'])

        if 'date__range' in self.request.GET:
            da_range = [
                parse_datetime(isodate)
                for isodate in self.request.GET['date__range'].split(',')
            ]
            queryset = queryset.filter(
                Q(creation_date__range=da_range)
                | Q(modification_date__range=da_range)
            )

        return queryset
