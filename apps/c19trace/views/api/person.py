import django_filters.rest_framework as filters
import rest_framework.filters as filters_drf
from django.conf import settings
from django.core import mail
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as gettext
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets, pagination
from rest_framework.response import Response

from ... import serializers, models
from ...rest import permissions
from ...util.api import api_view


class PersonSearchFilterset(filters.FilterSet):
    underage_person = filters.CharFilter(
        label=models.UnderagePerson._meta.verbose_name,
        lookup_expr='icontains', field_name='underage_persons__name'
    )

    class Meta:
        model = models.Person
        fields = ('document_no',)


class PersonSearchViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.Person
    queryset = models.Person.objects.all()
    permission_classes = [permissions.IsSuperuserOrTracerUser]
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.DjangoFilterBackend, filters_drf.SearchFilter]
    filterset_class = PersonSearchFilterset
    search_fields = (
        'names', 'first_surname', 'last_surname'
    )


class PersonViewSet(
    mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.Person
    queryset = models.Person.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                response: Response = super().create(request, *args, **kwargs)
                data = response.data
                data['mail_static_base'] = settings.MAIL_STATIC_BASE
                mail_html = render_to_string('mail/qr.html', data)

                mail.send_mail(
                    gettext("Digital ID for the Aysén region."),
                    strip_tags(mail_html),
                    settings.MAIL_FROM,
                    [data['email']],
                    html_message=mail_html
                )
        except:
            from traceback import print_exc
            print_exc()
            return Response(
                {
                    "non_field_errors": gettext(
                        "There is an error registring this person, "
                        "please try again later."
                    )
                },
                status=500
            )

        return response


@swagger_auto_schema(
    method="GET",
    responses={
        200: "If `document_no` exists",
        404: "If `document_no` doesn't exist"
    }
)
@api_view(http_method_names=["GET"])
def check_if_document_no_exists(request, document_no):
    return Response(
        status=(
            200 if models.Person.objects
                .filter(document_no=document_no)
                .values_list('id', flat=True)[0:1]
                .first()
            else 404
        )
    )