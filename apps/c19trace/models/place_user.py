from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .place import Place


class PlaceUser(models.Model):
    user = models.ForeignKey(
        User, verbose_name=gettext('User'), on_delete=models.CASCADE
    )
    place = models.ForeignKey(
        Place, verbose_name=gettext('Place'), on_delete=models.CASCADE
    )
    is_owner = models.BooleanField(
        verbose_name= gettext('Is owner')
    )

    class Meta:
        verbose_name = gettext("Place user")
        verbose_name_plural = gettext("Place users")

        db_table = 'c19t_place_users'
        ordering = ('place__name',)
