from django.contrib import admin
from .models import NegotiationRoom, SettlementProposal, ProposalResponse, NegotiationActivity

@admin.register(NegotiationRoom)
class NegotiationRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(SettlementProposal)
class SettlementProposalAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(ProposalResponse)
class ProposalResponseAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(NegotiationActivity)
class NegotiationActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

