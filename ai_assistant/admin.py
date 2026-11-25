from django.contrib import admin
from .models import AIAssistantSession, AISettlementDraft, TranslationJob

@admin.register(AIAssistantSession)
class AIAssistantSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(AISettlementDraft)
class AISettlementDraftAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(TranslationJob)
class TranslationJobAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

