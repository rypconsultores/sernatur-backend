from decimal import Decimal

from django.contrib.gis import admin as admin_geo
from django.contrib.gis.db import models as models_geo
from django.contrib.gis.forms import widgets as widgets_geo

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext

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
    model = models.PlaceUser
    extra = 0


class OSMWidgetAysen(widgets_geo.OSMWidget):
    template_name = 'gis/openlayers-osm.html'
    default_lon = Decimal("-72.0667")
    default_lat = Decimal("-45.5667")
    default_zoom = 15


class BingWidgetAysen(widgets_geo.OSMWidget):
    template_name = 'gis/openlayers-bing.html'
    bing_key = ''
    default_lon = Decimal("-72.0667")
    default_lat = Decimal("-45.5667")
    default_zoom = 15

    def __init__(self, attrs=None):
        super().__init__(attrs)

        if attrs and 'bing_key' in attrs:
            self.bing_key = attrs['bing_key']

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['bing_key'] = self.bing_key
        return context


class InlinePlaceCheckPoints(admin_geo.StackedInline):
    model = models.PlaceCheckPoint
    formfield_overrides = {
        models_geo.PointField: {"widget": OSMWidgetAysen}
    }
    extra = 0


class Place(admin_geo.OSMGeoAdmin):
    inlines = (
        InlinePlaceCheckPoints,
        InlineUserPlace,
    )

    list_display = ('place_type', 'name', 'comuna', 'localidad', 'zone', 'address')
    list_display_links = list_display

    class Media:
        model = models.Place


class TuristicServiceClass(admin.ModelAdmin):
    list_display = ('id', 'name', 'type_name', 'enabled_b')
    list_display_links = ('id', 'name', 'enabled_b')

    def type_name(self, instance):
        return mark_safe(
            f'<a href="../turisticservicetype/{instance.type.id}/change/">{instance.type.name}</a>'
        )
    type_name.admin_order_field = 'type__name'

    def enabled_b(self, instance):
        return gettext("Yes") if instance.enabled else gettext("No")
    enabled_b.admin_order_field = 'enabled'

    model = models.TuristicServiceClass


class TuristicServiceType(admin.ModelAdmin):
    list_display = ('id', 'name', 'enabled_b')
    list_display_links = list_display

    def enabled_b(self, instance):
        return gettext("Yes") if instance.enabled else gettext("No")
    enabled_b.admin_order_field = 'enabled'

    model = models.TuristicServiceType
