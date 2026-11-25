from django.contrib import admin
from .models import Subscription, APIKey, BulkDisputeImport

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(BulkDisputeImport)
class BulkDisputeImportAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

