from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .place import Place


class PlaceCheckPoint():
    name = models.CharField(
        verbose_name=gettext('Nombre'), max_length=96,
    )
    lon = models.DecimalField(
        verbose_name=gettext('Longitude'), max_digits=30,
        decimal_places=15
    )
    lat = models.DecimalField(
        verbose_name=gettext('Latitude'), max_digits=30,
        decimal_places=15
    )
    place = models.ForeignKey(
        Place, verbose_name=Place._meta.verbose_name,
        related_name='checkpoints'
    )

    class Meta:
        verbose_name = gettext("Place check point")
        verbose_name_plural = gettext("Place check points")

        db_table = 'c19t_place_check_point'
        ordering = ('name',)
