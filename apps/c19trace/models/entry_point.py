from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .common import transportation_modes
from .util import choices_to_helptext


class EntryPoint(models.Model):
    name = models.CharField(
        verbose_name=gettext("Name"), max_length=128,
        primary_key=True
    )
    type = models.CharField(
        verbose_name=gettext("Transportation mode"),
        max_length=64,
        choices=transportation_modes,
        help_text=choices_to_helptext(transportation_modes)
    )

    class Meta:
        verbose_name = gettext("Entry point")
        verbose_name_plural = gettext("Entry points")

        db_table = 'c19t_entry_point'
        ordering = ('name',)
