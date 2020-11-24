from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .service_type import ServiceType


class ServiceClass(models.Model):
    name = models.CharField(
        max_length=96, verbose_name=gettext("Name")
    )
    type = models.ForeignKey(
        ServiceType, verbose_name=ServiceType._meta.verbose_name,
        on_delete=models.PROTECT
    )
    enabled = models.BooleanField(
        verbose_name=gettext("Enabled"), default=True
    )

    class Meta:
        verbose_name = gettext("Service class")
        verbose_name_plural = gettext("Service classes")

        db_table = 'c19t_turistic_service_classes'
        ordering = ('name',)
