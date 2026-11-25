from django.contrib import admin
from .models import Complaint, ComplaintResponse, ComplaintAppeal, Feedback, GrievanceInvestigation

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(ComplaintResponse)
class ComplaintResponseAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(ComplaintAppeal)
class ComplaintAppealAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(GrievanceInvestigation)
class GrievanceInvestigationAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

