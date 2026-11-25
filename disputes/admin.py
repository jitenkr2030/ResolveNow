from django.contrib import admin
from .models import Dispute, DisputeParty, DisputeTimelineEntry

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(DisputeParty)
class DisputePartyAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(DisputeTimelineEntry)
class DisputeTimelineEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

