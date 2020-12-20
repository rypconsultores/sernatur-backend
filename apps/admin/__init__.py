"""
django-c19trace.rst admin file example.
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from . import c19trace
from ..c19trace import models


class AdminSite(admin.sites.AdminSite):
    site_title = _('SERNATUR Aysen: Traceability COVID19 Admin')

    # Text to put in each page's <h1> (and above login form).
    site_header = _('SERNATUR Aysen: Traceability COVID19 Admin')

    # Text to put at the top of the admin index page.
    index_title = _('Administration')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._registry.update(admin.site._registry)


site = AdminSite()

site.unregister(User)
site.register(User, c19trace.CustomUserAdmin)

for item in dir(c19trace):
    if hasattr(item, 'ignore_auto'):
        continue

    model_admin = getattr(c19trace, item)
    try:
        is_class = issubclass(model_admin, object)
    except TypeError:
        is_class = False

    if is_class and issubclass(model_admin, admin.ModelAdmin):
        try:
            site.register(getattr(models, item), model_admin)
        except:
            pass
