from copy import deepcopy

from django.db import models
from django.utils.translation import gettext_lazy as gettext

from .choices import underage_relationships
from .person import Person
from .util import choices_to_helptext


class UnderagePerson(models.Model):
    name = models.CharField(
        max_length=128, verbose_name=gettext("Name")
    )
    birth_date = models.DateField(
        verbose_name=gettext("Birth date")
    )
    relationship = models.CharField(
        max_length=24, verbose_name=gettext('Contact replationship'),
        choices=underage_relationships, help_text=(
                gettext('%s\n* Also can be filled with custom entry') % (
                choices_to_helptext(underage_relationships),
            )
        )
    )
    gender = deepcopy(Person._meta.get_field('gender'))
    related_to = models.ForeignKey(
        "Person", related_name="underage_persons", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = gettext("Underage person")
        verbose_name_plural = gettext("Underage persons")

        db_table = 'c19t_underage_person'
        ordering = ('name',)
