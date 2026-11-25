from django.contrib import admin
from .models import MediatorProfile, MediatorAvailability, MediatorFeedback, ConflictOfInterestDeclaration

@admin.register(MediatorProfile)
class MediatorProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(MediatorAvailability)
class MediatorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(MediatorFeedback)
class MediatorFeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(ConflictOfInterestDeclaration)
class ConflictOfInterestDeclarationAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

