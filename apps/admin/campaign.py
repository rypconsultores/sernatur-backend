from django.contrib import admin
from ..c19trace import models


class Entity(admin.ModelAdmin):
    list_display = ('code', 'name', 'flag')
    list_display_links = list_display

    class Media:
        model = models.Entity


class CampaignRequestType(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_display_links = list_display

    class Media:
        model = models.CampaignRequestType


class ProductSegment(admin.ModelAdmin):
    list_display = ('code', 'name', 'entity')
    list_display_links = list_display

    class Media:
        model = models.ProductSegment


class AffinityGroup(admin.ModelAdmin):
    list_display = ('code', 'name', 'entity')
    list_display_links = list_display

    class Media:
        model = models.AffinityGroup


class LiquidationModel(admin.ModelAdmin):
    list_display = ('code', 'name', 'cycle', 'entity')
    list_display_links = list_display

    class Media:
        model = models.LiquidationModel


class CampaignPromotionType(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_display_links = list_display

    class Media:
        model = models.CampaignPromotionType


class CampaignPaymentTypes(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_display_links = list_display

    class Media:
        model = models.CampaignPaymentTypes


class CampaignFinancialCostCharge(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_display_links = list_display

    class Media:
        model = models.CampaignFinancialCostCharge


class CampaignTransactionLimit(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_display_links = list_display

    class Media:
        model = models.CampaignTransactionLimit


class Market(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_display_links = list_display

    class Media:
        model = models.Market


class CampaignPaymentMethod(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_display_links = list_display

    class Media:
        model = models.CampaignPaymentMethod


class Establishment(admin.ModelAdmin):
    list_display = (
        'entity', 'pay_cycle_code', 'commerce_number',
        'market', 'CUIT', 'fee_percent', 'days_to_pay',
        'release_date', 'max_installments_count',
        'acquirer_manager', 'flag'
    )
    list_display_links = list_display

    class Media:
        model = models.Establishment