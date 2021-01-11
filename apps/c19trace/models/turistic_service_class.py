from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .turistic_service_type import TuristicServiceType


class TuristicServiceClass(models.Model):
    name = models.CharField(
        max_length=96, verbose_name=gettext("Name")
    )
    type = models.ForeignKey(
        TuristicServiceType, verbose_name=TuristicServiceType._meta.verbose_name,
        on_delete=models.PROTECT
    )
    enabled = models.BooleanField(
        verbose_name=gettext("Enabled"), default=True
    )

    def __str__(self):
        return f"{self.name} ({self.id})"

    class Meta:
        verbose_name = gettext("Service class")
        verbose_name_plural = gettext("Service classes")

        db_table = 'c19t_turistic_service_classes'
        ordering = ('name',)
