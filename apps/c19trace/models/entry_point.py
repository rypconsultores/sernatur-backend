from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .choices import transportation_modes, entry_point_types
from .util import choices_to_helptext


class EntryPoint(models.Model):
    name = models.CharField(
        verbose_name=gettext("Name"), max_length=128,
        primary_key=True
    )
    type = models.CharField(
        verbose_name=gettext("Transportation mode"),
        max_length=64,
        choices=entry_point_types,
        help_text=choices_to_helptext(entry_point_types)
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = gettext("Entry point")
        verbose_name_plural = gettext("Entry points")

        db_table = 'c19t_entry_point'
        ordering = ('name',)
