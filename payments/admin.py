from django.contrib import admin
from .models import Payment, RefundRequest, TaxInvoice, SubscriptionPlan

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(TaxInvoice)
class TaxInvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

