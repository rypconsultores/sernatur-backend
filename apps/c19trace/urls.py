

from django.urls import re_path, path, include
from django.utils.translation import gettext_lazy as gettext
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views

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
                r'places', views.api.place.PlaceViewSet,
                "api.places"
            ),
            (
                r'entry-points', views.api.entry_point.EntryPointViewSet,
                "api.entry_point"
            )
        ]).urls + [
            path('choices/', include([
                path('entry-point-types', views.api.choices.entry_point_types, name="api.choices.entry_point_types"),
                path('genders', views.api.choices.genders, name="api.choices.genders"),
                path('relationships', views.api.choices.relationships, name="api.choices.relationships"),
                path('residence-choices', views.api.choices.residence_choices, name="api.choices.residence_choices"),
                path('transportation-means', views.api.choices.transportation_means, name="api.choices.transportation_means"),
                path('transportation-modes', views.api.choices.transportation_modes, name="api.choices.transportation_modes"),
                path('travel-documents', views.api.choices.travel_documents, name="api.choices.travel_documents"),
                path('underage-relationships', views.api.choices.underage_relationships, name="api.choices.underage_relationships"),
                path('travel-subject', views.api.choices.travel_subject, name="api.choices.travel_subject"),
            ])),
            path('auth/', include([
                path('token/', include([
                    path('', views.api.auth.TokenObtainPairCustomView.as_view(), name='api.auth.token'),
                    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='api.auth.token.refresh'),
                    path('destroy/', jwt_views.TokenRefreshView.as_view(), name='api.auth.token.destroy'),
                ]))
            ])),
            path(
                'persons', views.api.person.PersonSearchViewSet.as_view({"get": "list"}),
                name="api.places.persons.search"
            ),
            path(
                'places/<int:id>/persons/', views.api.place.place_add_person,
                name="api.places.persons.add"
            ),
            path(
                'places/<int:id>/persons/<person_id>/', views.api.place.place_delete_person,
                name="api.places.persons.delete"
            ),
            path(
                'places/by-person-check/<id>/', views.api.place_person_check.by_person,
                name="api.places.by_person_check.list"
            ),
            path(
                'places/<int:place_id>/person/checks/',
                views.api.place_person_check.PlacePersonCheckViewSetByPlace.as_view({"get": "list"}),
                name="api.user.places.list"
            ),
            path(
                'places/<int:place_id>/person/checks/<person_id>/'
                , views.api.place_person_check.check_upsert
                , name="api.places.person.check.upsert"
            ),
            path(
                'places/<int:place_id>/person/checks/<person_id>/<check_id>/'
                , views.api.place_person_check.check_retrieve
                , name="api.places.person.check.retrieve"
            ),
            path(
                'places/<int:id>/stats/'
                , views.api.place.stats
                , name="api.places.stats"
            ),
            path('places/turistic/service/', include(
                routers.DefaultRouter([
                    (
                        r'types', views.api.place.TuristicServiceTypeViewSet,
                        "api.places.turistic.services.type"
                    ),
                    (
                        r'classes', views.api.place.TuristicServiceClassViewSet,
                        "api.places.turistic.services.class"
                    ),
                ]).urls
            )),
            path('user/password/', include([
                path('change-or-create/', include([
                    path(
                         '', views.api.user.password_create_or_replace_request,
                         name="api.user.password.change_or_create"
                    ),
                    path(
                        '<id>/', views.api.user.PasswordChangeOrCreate.as_view(),
                        name="api.user.password.change_or_create.item"
                    )
                ]))
            ])),
            path(
                'person/<id>/places/',
                views.api.place_person_check.PlacePersonCheckViewSetByUser.as_view({"get": "list"}),
                name="api.user.places.list"
            ),
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