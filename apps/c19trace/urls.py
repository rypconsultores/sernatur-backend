

from django.urls import re_path, path, include
from django.utils.translation import gettext_lazy as gettext
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views
from .rest import routers


schema_view = get_schema_view(
   openapi.Info(
      title=gettext("SERNATUR COVID19 traceability API"),
      default_version='1.0.0',
      description=gettext("For mobile and web app."),
      #terms_of_service="https://www.google.com/policies/terms/",
      #contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="Commercial"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


api_path = path(
    'api/', include(
        routers.DefaultRouter([
            (
                r'person', views.api.person.PersonViewSet,
                "api.person"
            ),
            (
                r'entry-points', views.api.entry_point.EntryPointViewSet,
                "api.entry_point"
            ),
        ]).urls + [
            path('choices/', include([
                path('relationships', views.api.choices.relationships, name="api.choices.relationships"),
                path('underage-relationships', views.api.choices.underage_relationships, name="api.choices.underage_relationships"),
                path('transportation-modes', views.api.choices.transportation_modes, name="api.choices.transportation_modes"),
                path('genders', views.api.choices.genders, name="api.choices.genders"),
                path('travel-documents', views.api.choices.travel_documents, name="api.choices.travel_documents"),
                path('residence-choices', views.api.choices.residence_choices, name="api.choices.residence_choices"),
                path('transportation-means', views.api.choices.transportation_means, name="api.choices.transportation_means"),
                path('entry-point-types', views.api.choices.entry_point_types, name="api.choices.entry_point_types"),
            ]))
        ]
    )
)

api_path.url_patterns.append(
    path('specs/', include([
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='api.schema.file'),
        path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='api.schema.swaggerui'),
        path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='api.schema.redoc'),
    ]))
)

urlpatterns = [
    #path('', views.api.dashboard, name="app.dashboard"),
    #path('reports', views.app.reports, name="app.reports"),
    #path('imeilogs/<start_date>/<end_date>', views.app.imeilogs, name="app.imeilogs"),
    #path('login', views.app.login_view, name="app.login"),
    #path('logout', views.app.logout_view, name="app.logout"),
    api_path
]