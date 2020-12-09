from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .turistic_service_class import TuristicServiceType, TuristicServiceClass
from .util import choices_to_helptext


class Place(models.Model):
    PLACE_TYPE_TURISTIC_SERVICE = 1
    PLACE_TYPE_TURIST_ATTRACTION = 2
    PLACE_TYPE_TURISTIC_INFO_OFFICE = 3
    PLACE_TYPE_HEALTH_PLACE = 4
    PLACE_TYPE_CHECK_POINT_MUNICIPAL = 5
    PLACE_TYPE_SANITARY_CHECK_POINT = 6
    PLACE_TYPE_BORDER_CROSSING = 7

    _entity_type_choices = (
        (PLACE_TYPE_TURISTIC_SERVICE, gettext("Turistic service")),
        (PLACE_TYPE_TURIST_ATTRACTION, gettext('Turist attraction')),
        (PLACE_TYPE_TURISTIC_INFO_OFFICE, gettext('Turistic information office')),
        (PLACE_TYPE_HEALTH_PLACE, gettext("Health place")),
        (PLACE_TYPE_CHECK_POINT_MUNICIPAL, gettext('Check point municipal')),
        (PLACE_TYPE_SANITARY_CHECK_POINT, gettext('Sanitary check point')),
        (PLACE_TYPE_BORDER_CROSSING, gettext('Border crossing')),
    )
    place_type = models.IntegerField(
        verbose_name=gettext('Place type'),
        choices=_entity_type_choices,
        help_text=choices_to_helptext(_entity_type_choices)
    )
    _turistic_info_office_type = (
        ('SERNATUR', 'SERNATUR'),
        ('MUNICIPAL', 'MUNICIPAL'),
        ('GREMIO', 'GREMIO')
    )
    turistic_info_office_type = models.CharField(
        max_length=16, verbose_name=gettext('Turistic information office type'),
        choices=_turistic_info_office_type,
        help_text=choices_to_helptext(_turistic_info_office_type),
        null=True, blank=True
    )
    rut = models.CharField(
        max_length=15, verbose_name=gettext("RUT Entity")
    )
    service_type = models.ForeignKey(
        TuristicServiceType, verbose_name=TuristicServiceType._meta.verbose_name, on_delete=models.CASCADE
    )
    service_class = models.ForeignKey(
        TuristicServiceClass, verbose_name=TuristicServiceClass._meta.verbose_name, on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=128, verbose_name=gettext("Name")
    )
    comuna = models.CharField(
        max_length=128, verbose_name=gettext("Comuna")
    )
    localidad = models.CharField(
        max_length=128, verbose_name=gettext("Localidad"), null=True, blank=True
    )
    zone = models.CharField(
        max_length=98, verbose_name=gettext("Zone"), null=True, blank=True
    )
    address = models.CharField(
        max_length=128, verbose_name=gettext("Address"), null=True, blank=True
    )
    representative_name = models.CharField(
        max_length=128, verbose_name=gettext("Representative: Name")
    )
    representative_position = models.CharField(
        max_length=128, verbose_name=gettext("Representative: Position")
    )
    representative_phone = models.CharField(
        max_length=45, verbose_name=gettext("Representative: Phone")
    )
    representative_mail = models.CharField(
        max_length=128, verbose_name=gettext("Representative: Mail")
    )
    users = models.ManyToManyField(
        User, through='PlaceUser', verbose_name=gettext("Users"),
        related_name='places'
    )

    class Meta:
        verbose_name = gettext("Place")
        verbose_name_plural = gettext("Places")

        db_table = 'c19t_places'
        ordering = ('name',)
