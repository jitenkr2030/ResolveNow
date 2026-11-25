from django.contrib import admin
from .models import MediatorAssignmentRequest, MediatorReplacementRequest, AssignmentHistory

@admin.register(MediatorAssignmentRequest)
class MediatorAssignmentRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(MediatorReplacementRequest)
class MediatorReplacementRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(AssignmentHistory)
class AssignmentHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

