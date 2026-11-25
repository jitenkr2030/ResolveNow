from django.contrib import admin
from .models import MediationRoom, RoomParticipant, SessionNote, PrivateCaucus

@admin.register(MediationRoom)
class MediationRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(RoomParticipant)
class RoomParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(SessionNote)
class SessionNoteAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(PrivateCaucus)
class PrivateCaucusAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

