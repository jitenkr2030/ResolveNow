from django.contrib import admin
from .models import CaseTransfer, CaseWithdrawalRequest, CaseReopeningRequest, CaseReminder, CaseNote, CaseArchive

@admin.register(CaseTransfer)
class CaseTransferAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(CaseWithdrawalRequest)
class CaseWithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(CaseReopeningRequest)
class CaseReopeningRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(CaseReminder)
class CaseReminderAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(CaseNote)
class CaseNoteAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(CaseArchive)
class CaseArchiveAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

