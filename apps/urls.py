"""
URL Configuration for proeject
"""

from apps import admin
from django.urls import path, include
import apps.c19trace.urls

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('', include(apps.c19trace.urls))
]
