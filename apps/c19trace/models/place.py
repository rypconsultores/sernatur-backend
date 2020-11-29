from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .service_class import ServiceType
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
        (PLACE_TYPE_SANITARY_CHECK_POINT, gettext('Sanitary check point ')),
        (PLACE_TYPE_BORDER_CROSSING, gettext('Border crossing')),
    )
    place_type = models.IntegerField(
        verbose_name=gettext('Entity type'),
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
        help_text=choices_to_helptext(_turistic_info_office_type)
    )
    rut = models.CharField(
        max_length=15, verbose_name=gettext("RUT Entity")
    )
    service_type = models.ForeignKey(
        ServiceType, verbose_name=ServiceType._meta.verbose_name, on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=128, verbose_name=gettext("Name")
    )
    comuna = models.CharField(
        max_length=128, verbose_name=gettext("Comuna")
    )
    localidad = models.CharField(
        max_length=128, verbose_name=gettext("Localidad"), null=True
    )
    zone = models.CharField(
        max_length=98, verbose_name=gettext("Zone"), null=True
    )
    address = models.CharField(
        max_length=128, verbose_name=gettext("Address"), null=True
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
        User, through='UserPlace', verbose_name=gettext("Users"),
        related_name='places'
    )

    class Meta:
        verbose_name = gettext("Place entity")
        verbose_name_plural = gettext("Place entities")

        db_table = 'c19t_place_entity'
        ordering = ('name',)
