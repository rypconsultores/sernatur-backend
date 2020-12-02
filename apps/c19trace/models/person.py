from uuid import uuid4

from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as gettext

from .choices import (
    relationships, transportation_modes, genders, travel_documents,
    residence_choices, transportation_means
)
from .entry_point import EntryPoint
from .util import choices_to_helptext, thenow


class Person(models.Model):
    id = models.CharField(
        max_length=64, verbose_name=gettext("ID"), primary_key=True,
        default='__noid__'
    )
    date = models.DateTimeField(
        default=thenow, verbose_name=gettext("Date/Time")
    )
    first_surname = models.CharField(
        max_length=48, verbose_name=gettext("First surname")
    )
    last_surname = models.CharField(
        max_length=48, verbose_name=gettext("Last surname"), null=False
    )
    names = models.CharField(
        max_length=64, verbose_name=gettext("Names")
    )
    gender = models.CharField(
        max_length=24, verbose_name=gettext("Gender"),
        choices=genders,
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
        choices=travel_documents,
        help_text=choices_to_helptext(travel_documents)
    )
    document_no = models.CharField(
        max_length=128, verbose_name=gettext("Document Number")
    )
    residence = models.CharField(
        max_length=24, verbose_name=gettext("Residence place"),
        choices=residence_choices,
        help_text=choices_to_helptext(residence_choices)
    )
    residence_chile_region = models.CharField(
        max_length=2, verbose_name=gettext("Residence in Chile: Region"), null=True
    )
    residence_chile_comuna = models.CharField(
        max_length=64, verbose_name=gettext("Residence in Chile: Comuna"), null=True
    )
    residence_other_country = models.CharField(
        max_length=64, verbose_name=gettext("Residence outside Chile: Country"), null=True
    )
    residence_other_place = models.CharField(
        max_length=128, verbose_name=gettext("Residence outside Chile: Place"), null=True
    )
    email = models.CharField(
        max_length=128, verbose_name=gettext("Email")
    )
    mobile_phone = models.CharField(
        max_length=128, verbose_name=gettext("Mobile Phone")
    )
    previous_lodging_place = models.CharField(
        max_length=128, verbose_name=gettext("Previous lodging place")
    )
    visit_subject = models.CharField(
        max_length=128, verbose_name=gettext("Visit subject")
    )
    visit_no = models.IntegerField(
        verbose_name=gettext("Visit number")
    )
    transportation_mode = models.CharField(
        max_length=8,
        verbose_name=gettext("Transportation mode"),
        choices=transportation_modes,
        help_text=choices_to_helptext(transportation_modes)
    )
    destination = models.IntegerField(
        verbose_name=gettext("Destination")
    )
    entry_point = models.ForeignKey(
        EntryPoint, verbose_name=gettext("Entry point"), on_delete=models.CASCADE
    )
    main_transportation_mean = models.CharField(
        verbose_name=gettext("Main transportation mean"), max_length=64,
        choices=transportation_means, help_text=(
            gettext('%s\n* Also can be filled with custom entry') % (
                choices_to_helptext(transportation_means),
            )
        )
    )
    contact_name = models.CharField(
        verbose_name=gettext("Contact Name"), max_length=128
    )
    contact_relationship = models.CharField(
        max_length=24, verbose_name=gettext('Contact replationship'),
        choices=relationships, help_text=(
            gettext('%s\n* Also can be filled with custom entry') % (
                choices_to_helptext(relationships),
            )
        )
    )
    contact_phone_or_email = models.CharField(
        max_length=24, verbose_name=gettext('Contact phone or email')
    )
    contact_comuna = models.CharField(
        max_length=24, verbose_name=gettext('Contact comuna'), blank=True, null=True
    )
    contact_localidad = models.CharField(
        max_length=24, verbose_name=gettext('Contact localidad'), blank=True, null=True
    )

    def create_id(self):
        return (
            'R' if 'aysen' in self.residence_chile_region.lower() else 'NR'
            + thenow().strftime("%Y%m%d")
            + self.name[0:1].upper()
            + self.first_surname[0:1].upper()
            + uuid4().hex
        )

    class Meta:
        verbose_name = gettext("Person")
        verbose_name_plural = gettext("Person")

        db_table = 'c19t_persons'
        ordering = ('names', 'first_surname', 'last_surname')


@receiver(models.signals.pre_save, sender=Person)
def voucher_actions(
    sender, instance, raw, using, update_fields, **kwargs
):
     if instance.id == '__noid__':
         instance.id = instance.create_id()
