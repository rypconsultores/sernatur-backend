from django.contrib.gis.db import models as models_geo
from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .place import Place


class PlaceCheckPoint(models_geo.Model):
    name = models.CharField(
        verbose_name=gettext('Nombre'), max_length=96,
    )
    location = models_geo.PointField(
        verbose_name=gettext('Location'), srid=4326
    )
    place = models.ForeignKey(
        Place, verbose_name=Place._meta.verbose_name,
        related_name='check_points', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = gettext("Place check point")
        verbose_name_plural = gettext("Place check points")

        db_table = 'c19t_place_check_point'
        ordering = ('name',)
