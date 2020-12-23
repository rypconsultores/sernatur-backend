from urllib.parse import urlparse, urlunparse

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as gettext
from drf_yasg.utils import swagger_auto_schema
from rest_framework import views
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.c19trace.util.api import api_view
from ... import models
from ... import serializers


@swagger_auto_schema(
    method="POST",
    request_body=serializers.PasswordChangeOrCreateRequest,
    responses={
        201: serializers.PasswordChangeOrCreate,
        429: "Too much requests (maximum per day exceeded)"
    }
)
@api_view(http_method_names=['POST'])
def password_create_or_replace_request(request):
    serializers.PasswordChangeOrCreateRequest(data=request.data).is_valid(True)
    person: models.Person = get_object_or_404(
        models.Person.objects, email=request.data['email'],
        document_no=request.data['document_no']
    )

    password_request_kwargs = {
        "user": person.user,
        "person": None if person.user else person
    }

    if (
        (
            models.PasswordChangeOrCreate\
                .objects\
                .filter(**password_request_kwargs)\
                .count()
        ) >= settings.USER_PASSWORD_REQUEST_MAX_PER_DAY
    ):
        return Response(
            {"non_field_errors": [gettext("Enough password requests for today.")]},
            status=429
        )

    try:
        with transaction.atomic() as trx:
            password_request = models.PasswordChangeOrCreate(
                user=person.user, person=None if person.user else person
            )
            password_request.save()

            data = serializers.Person(instance=person).data
            data['mail_static_base'] = settings.MAIL_STATIC_BASE

            url_object = urlparse(
                    request.META.get(
                        'HTTP_REFERER', settings.FRONTEND_URL_BASE
                    )
                ) \
                ._replace(path=f'/change-password/{password_request.id}')

            action = gettext("change") if person.user else gettext("create")
            data.update({
                "action": action,
                "set_password_link": urlunparse(url_object),
                "set_password_key": password_request.key
            })

            mail_html = render_to_string('mail/password.html', data)
            mail.send_mail(
                gettext("%s request for password" % (action.title())),
                strip_tags(mail_html),
                settings.MAIL_FROM,
                [person.email],
                html_message=mail_html
            )
    except:
        import traceback as tb;tb.print_exc()
        return Response(
            {"non_field_errors": [gettext("Unexpected internal error, try again")]},
            status=500
        )
    else:
        return Response(
            {"id": password_request.id},
            status=201
        )


class PasswordChangeOrCreate(views.APIView):
    @swagger_auto_schema(
        responses={
            200: serializers.PasswordChangeOrCreate
        }
    )
    def get(self, request, id):
        return Response(
            serializers.PasswordChangeOrCreate(
                instance=get_object_or_404(models.PasswordChangeOrCreate.objects.all(), id=id)
            ).data
        )

    @swagger_auto_schema(
        request_body=serializers.PasswordSet,
        responses={204: "No content"}
    )
    def post(self, request, id):
        instance = get_object_or_404(
            models.PasswordChangeOrCreate.objects,
            id=id, key=request.data.get('key')
        )

        if not instance.user:
            instance.user = User(
                first_name=instance.person.names,
                last_name=instance.person.first_surname,
                email=instance.person.email,
                username=instance.person.document_no
            )
            instance.user.save()
            instance.person.user = instance.user
            instance.person.save()

        instance.user.set_password(request.data.get("password"))
        instance.user.save()
        instance.delete()

        return Response(status=204)

