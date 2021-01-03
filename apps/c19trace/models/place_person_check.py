from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as gettext

from .place_check_point import PlaceCheckPoint
from .person import Person
from .place import Place
from .util import thenow


class PlacePersonCheckSymptom(models.Model):
    cough = models.BooleanField(
        verbose_name=gettext("Cough"), default=False
    )
    dispnea = models.BooleanField(
        verbose_name=gettext("Dispnea or breathing difficulty"), default=False
    )
    thoracic_pain = models.BooleanField(
        verbose_name=gettext("Throracic pain"), default=False
    )
    throat_pain = models.BooleanField(
        verbose_name=gettext("Throat pain or odynophagia"), default=False
    )
    muscular_articular_pain = models.BooleanField(
        verbose_name=gettext("Myalgia, muscular or articular pain"), default=False
    )
    chills = models.BooleanField(
        verbose_name=gettext("Chills"), default=False
    )
    headache = models.BooleanField(
        verbose_name=gettext("Headache"), default=False
    )
    diarrhea = models.BooleanField(
        verbose_name=gettext("Diarrhea"), default=False
    )
    lost_smell = models.BooleanField(
        verbose_name=gettext("Abrupt lost of smell"), default=False
    )
    lost_taste = models.BooleanField(
        verbose_name=gettext("Abrupt lost of taste"), default=False
    )
    fever = models.BooleanField(
        verbose_name=gettext("fever"), default=False
    )

    class Meta:
        verbose_name = gettext("Place person check symptoms")
        verbose_name_plural = gettext("Place persons checks symptoms")

        db_table = 'c19t_place_persons_checks_symptoms'


class PlacePersonCheck(models.Model):
    id = models.CharField(
        max_length=64, verbose_name=gettext("ID"), primary_key=True
    )
    creation_date = models.DateTimeField(
        default=thenow, verbose_name=gettext("Creation date")
    )
    modification_date = models.DateTimeField(
        default=thenow, verbose_name=gettext("Modification date")
    )
    place = models.ForeignKey(
        Place, verbose_name=Place._meta.verbose_name, on_delete=models.CASCADE
    )
    place_check_point = models.ForeignKey(
        PlaceCheckPoint, verbose_name=Place._meta.verbose_name, on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        Person, verbose_name=Person._meta.verbose_name, on_delete=models.CASCADE,
        related_name='persons_checks'
    )
    symptoms = models.OneToOneField(
        PlacePersonCheckSymptom, verbose_name=gettext("Symptoms"),
        on_delete=models.RESTRICT
    )
    is_customer = models.BooleanField(
        verbose_name=gettext("Es cliente"), default=False
    )
    is_employee = models.BooleanField(
        verbose_name=gettext("Es trabajador"), default=False
    )
    is_provider = models.BooleanField(
        verbose_name=gettext("Es proovedor"), default=False
    )
    observations = models.TextField(
        verbose_name=gettext("Observations"), null=True, blank=True
    )

    class Meta:
        verbose_name = gettext("Place person check")
        verbose_name_plural = gettext("Place persons checks")

        db_table = 'c19t_place_persons_checks'
        ordering = ('creation_date',)


@receiver(models.signals.pre_save, sender=Person)
def place_person_check_auto_mod_date(
    sender, instance: PlacePersonCheck, raw, using, update_fields, **kwargs
):
     instance.modification_date = thenow()
