from django.contrib import admin
from .models import AuditLog, SystemConfigurationLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(SystemConfigurationLog)
class SystemConfigurationLogAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

