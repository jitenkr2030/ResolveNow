from django.contrib import admin
from .models import DisputeCategory, LegalEligibilityChecklist, DisputeEligibilityResult

@admin.register(DisputeCategory)
class DisputeCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(LegalEligibilityChecklist)
class LegalEligibilityChecklistAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(DisputeEligibilityResult)
class DisputeEligibilityResultAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

