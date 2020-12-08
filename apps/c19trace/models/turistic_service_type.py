from django.db import models
from django.utils.translation import gettext_lazy as gettext


class TuristicServiceType(models.Model):
    name = models.CharField(
        max_length=96, verbose_name=gettext("Name")
    )
    enabled = models.BooleanField(
        verbose_name=gettext("Enabled"), default=True
    )

    class Meta:
        verbose_name = gettext("Service type")
        verbose_name_plural = gettext("Service types")

        db_table = 'c19t_turistic_service_types'
        ordering = ('name',)
