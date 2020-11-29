from django.contrib.gis.forms.widgets import OSMWidget

from django.contrib import admin
from ..c19trace import models


class EntryPoint(admin.ModelAdmin):
    list_display = ('pk', 'name', 'type')
    list_editable = ('name', 'type')
    list_display_links = ('pk',)

    class Media:
        model = models.EntryPoint


class InlineUnderagePerson(admin.TabularInline):
    model = models.UnderagePerson
    extra = 0


class Person(admin.ModelAdmin):
    inlines = (
        InlineUnderagePerson,
    )

    list_display = ('names', 'first_surname', 'last_surname')
    list_display_links = list_display

    class Media:
        model = models.Person


class InlineUserPlace(admin.TabularInline):
    model = models.UserPlace
    extra = 0


class InlinePlaceCheckPoints(admin.TabularInline):
    model = models.PlaceCheckPoint
    formfield_overrides = {
        "location": {"widget": OSMWidget}
    }


class Place(admin.ModelAdmin):
    inlines = (
        InlineUserPlace,
    )

    list_display = ('place_type', 'name', 'comuna', 'localidad', 'zone', 'address')
    list_display_links = list_display

    class Media:
        model = models.Place
