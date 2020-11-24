from django.urls import re_path, path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views
from .rest import routers

"""
schema_view = get_schema_view(
   openapi.Info(
      title="PRISMA Campaigns API",
      default_version='1.0.0',
      description="For marketing campaigns.",
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
                r'entities', views.api.common.EntityViewSet,
                "api.client.imei"
            ), (
                'product-segment', views.api.common.ProductSegmentViewSet,
                'api.product-segment'
            ), (
                'affinity-group', views.api.common.AffinityGroupViewSet,
                'api.affinity-group'
            ), (
                'liquidation-model', views.api.common.LiquidationModelViewSet,
                'api.liquidation-model'
            ), (
                'emitter-c19trace', views.api.emitter_campaign.EmitterCampaignViewSet,
                'api.emitter-c19trace'
            ), (
                'acquirer-c19trace', views.api.acquirer_campaign.AcquirerCampaignViewSet,
                'api.acquirer-c19trace'
            ), (
                'market', views.api.common.MarketViewSet,
                'api.c19trace-market'
            ), (
                'establishment', views.api.establishment.EstablishmentViewSet,
                'api.establishment'
            ), (
                'terminal', views.api.establishment.EstablishmentTerminalViewSet,
                'api.establishment.terminal'
            )
        ]).urls + [
            path('campaigns/', include(
                routers.DefaultRouter([
                    (
                        'request-type', views.api.common.CampaignRequestTypeViewSet,
                        'api.request-type'
                    ), (
                        'promotion-type', views.api.common.CampaignPromotionTypeViewSet,
                        'api.c19trace-promotion-type'
                    ), (
                        'payment-types', views.api.common.CampaignPaymentTypesViewSet,
                        'api.c19trace-payment-types'
                    ), (
                        'financial-cost-charge', views.api.common.CampaignFinancialCostChargeViewSet,
                        'api.c19trace-financial-cost-charge'
                    ), (
                        'transaction-limit', views.api.common.CampaignTransactionLimitViewSet,
                        'api.c19trace-transaction-limit'
                    ), (
                        'payment-data_set', views.api.common.CampaignPaymentMethodViewSet,
                        'api.c19trace-payment-data_set'
                    ),
                ]).urls
            )),
            re_path(r"^emitter-c19trace/(?P<id>\d+?)/cobol-data/(?P<data_set>.*?).txt", views.api.cobol_data,
                name="api.emitter-c19trace.cobol-data", kwargs={"object_type": "emitter-c19trace"}
            ),
            re_path(r"^acquirer-c19trace/(?P<id>\d+?)/cobol-data/(?P<data_set>.*?).txt", views.api.cobol_data,
                name="api.acquirer_campaign.cobol-data", kwargs={"object_type": "acquirer-c19trace"}
            )
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
"""
urlpatterns = []