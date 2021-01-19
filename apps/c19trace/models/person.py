from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as gettext

from .choices import (
    relationships, transportation_modes, genders, travel_documents,
    residence_choices, transportation_means, travel_subject
)
from .entry_point import EntryPoint
from .util import (
    choices_to_helptext, thenow, password_request_id, password_request_expiracy,
    password_request_key
)

person_auto_id_wildcard = '__auto__'


class Person(models.Model):
    id = models.CharField(
        max_length=64, verbose_name=gettext("ID"), primary_key=True,
        default=person_auto_id_wildcard
    )
    date = models.DateTimeField(
        default=thenow, verbose_name=gettext("Date/Time")
    )
    first_surname = models.CharField(
        max_length=48, verbose_name=gettext("First surname")
    )
    last_surname = models.CharField(
        max_length=48, verbose_name=gettext("Last surname"), null=True, blank=True
    )
    names = models.CharField(
        max_length=64, verbose_name=gettext("Names")
    )
    gender = models.CharField(
        max_length=24, verbose_name=gettext("Gender"),
#        choices=genders,
        help_text=choices_to_helptext(genders)
    )
    birth_date = models.DateField(
        verbose_name=gettext("Birth date")
    )
    nationality = models.CharField(
        max_length=3, verbose_name=gettext("Nationality"),
    )
    travel_document = models.CharField(
        max_length=16, verbose_name=gettext("Travel document"),
#        choices=travel_documents,
        help_text=choices_to_helptext(travel_documents)
    )
    document_no = models.CharField(
        max_length=128, verbose_name=gettext("Document Number"), unique=True
    )
    residence = models.CharField(
        max_length=24, verbose_name=gettext("Residence place"),
        choices=residence_choices,
        help_text=choices_to_helptext(residence_choices)
    )
    residence_chile_region = models.CharField(
        max_length=2, verbose_name=gettext("Residence in Chile: Region"), null=True, blank=True
    )
    residence_chile_comuna = models.CharField(
        max_length=64, verbose_name=gettext("Residence in Chile: Comuna"), null=True, blank=True
    )
    residence_other_country = models.CharField(
        max_length=64, verbose_name=gettext("Residence outside Chile: Country"), null=True, blank=True
    )
    residence_other_place = models.CharField(
        max_length=128, verbose_name=gettext("Residence outside Chile: Place"), null=True, blank=True
    )
    email = models.CharField(
        max_length=128, verbose_name=gettext("Email")
    )
    mobile_phone = models.CharField(
        max_length=128, verbose_name=gettext("Mobile Phone")
    )
    previous_lodging_place = models.CharField(
        max_length=128, verbose_name=gettext("Previous lodging place"), null=True, blank=True
    )
    visit_subject = models.CharField(
        max_length=128, verbose_name=gettext("Visit subject"),
        #Wchoices=travel_subject,
        null=True, blank=True
    )
    visit_no = models.CharField(
        max_length=12, verbose_name=gettext("Visit number"), null=True, blank=True
    )
    transportation_mode = models.CharField(
        max_length=8,
        verbose_name=gettext("Transportation mode"),
        choices=transportation_modes,
        help_text=choices_to_helptext(transportation_modes),
        null=True, blank=True
    )
    destination = models.CharField(
        max_length=128, verbose_name=gettext("Destination"),
        null=True, blank=True
    )
    entry_point = models.ForeignKey(
        EntryPoint, verbose_name=gettext("Entry point"), on_delete=models.CASCADE,
        null=True, blank=True
    )
    main_transportation_mean = models.CharField(
        verbose_name=gettext("Main transportation mean"), max_length=64,
        # choices=transportation_means,
        help_text=(
            gettext('%s\n* Also can be filled with custom entry') % (
                choices_to_helptext(transportation_means),
            )
        ),
        null=True, blank=True
    )
    contact_name = models.CharField(
        verbose_name=gettext("Contact Name"), max_length=128, null=True, blank=True
    )
    contact_relationship = models.CharField(
        max_length=48, verbose_name=gettext('Contact replationship'),
        #choices=relationships,
        help_text=(
            gettext('%s\n* Also can be filled with custom entry') % (
                choices_to_helptext(relationships),
            )
        ),
        null=True, blank=True
    )
    contact_phone_or_email = models.CharField(
        max_length=24, verbose_name=gettext('Contact phone or email'), blank=True, null=True
    )
    contact_comuna = models.CharField(
        max_length=24, verbose_name=gettext('Contact comuna'), blank=True, null=True
    )
    contact_localidad = models.CharField(
        max_length=24, verbose_name=gettext('Contact localidad'), blank=True, null=True
    )
    user = models.OneToOneField(
        User, verbose_name=gettext('User'), on_delete=models.CASCADE, blank=True, null=True
    )

    def create_id(self):
        return (
            'R' if (
                self.residence_chile_region
                and 'aysen' in self.residence_chile_region.lower()
            ) else 'NR'
            + thenow().strftime("%Y%m%d")
            + self.names[0:1].upper()
            + self.first_surname[0:1].upper()
            + uuid4().hex.upper()
        )

    def __str__(self):
        description = f"{self.names} {self.first_surname}"
        if self.last_surname:
            description = f"{description} {self.last_surname}"

        return f"{description} ({self.id})"

    class Meta:
        verbose_name = gettext("Person")
        verbose_name_plural = gettext("Person")

        db_table = 'c19t_persons'
        ordering = ('names', 'first_surname', 'last_surname')


@receiver(models.signals.pre_save, sender=Person)
def person_auto_make_id(
    sender, instance, raw, using, update_fields, **kwargs
):
     if instance.id == person_auto_id_wildcard:
         instance.id = instance.create_id()


class PasswordChangeOrCreate(models.Model):
    id = models.CharField(
        verbose_name=gettext("ID"), max_length=64, default=password_request_id,
        primary_key=True
    )

    key = models.CharField(
        verbose_name=gettext("Key"), max_length=128, default=password_request_key
    )

    expires = models.DateTimeField(
        verbose_name=gettext("Expires"), default=password_request_expiracy
    )

    user = models.ForeignKey(
        User, verbose_name=gettext("User"), on_delete=models.CASCADE, null=True
    )

    person = models.ForeignKey(
        Person, verbose_name=gettext("Person"), on_delete=models.CASCADE, null=True
    )

    class Meta:
        verbose_name = gettext("Password request")
        verbose_name_plural = gettext("Password requests")

        db_table = 'c19t_password_change_or_create'
        ordering = ('-expires', 'user')
