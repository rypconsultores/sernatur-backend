"""
URL Configuration for proeject
"""
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

import apps.c19trace.urls
from apps import admin

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('js/i18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),

    path('', include(apps.c19trace.urls))
]
