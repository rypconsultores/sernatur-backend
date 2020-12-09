from django.conf import settings
from django.core import mail
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as gettext
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from ... import serializers, models


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