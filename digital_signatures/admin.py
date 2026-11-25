from django.contrib import admin
from .models import DigitalSignature

@admin.register(DigitalSignature)
class DigitalSignatureAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

