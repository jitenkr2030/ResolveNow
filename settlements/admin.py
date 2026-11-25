from django.contrib import admin
from .models import SettlementRecord, SettlementSignature, SettlementComplianceRecord

@admin.register(SettlementRecord)
class SettlementRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(SettlementSignature)
class SettlementSignatureAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(SettlementComplianceRecord)
class SettlementComplianceRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

