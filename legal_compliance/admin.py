from django.contrib import admin
from .models import ConsentRecord, DataSubjectRequest, DataRetentionPolicy, SecurityIncident, ConflictOfInterestDeclaration

@admin.register(ConsentRecord)
class ConsentRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(DataSubjectRequest)
class DataSubjectRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(DataRetentionPolicy)
class DataRetentionPolicyAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(SecurityIncident)
class SecurityIncidentAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(ConflictOfInterestDeclaration)
class ConflictOfInterestDeclarationAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

