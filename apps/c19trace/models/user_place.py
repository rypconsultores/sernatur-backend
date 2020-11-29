from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .place import Place


class UserPlace(models.Model):
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
        verbose_name = gettext("User place")
        verbose_name_plural = gettext("User places")

        db_table = 'c19t_user_place'
        ordering = ('place__name',)
