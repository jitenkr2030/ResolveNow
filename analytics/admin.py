from django.contrib import admin
from .models import AnalyticsSnapshot, CategoryAnalytics, MediatorPerformanceMetric

@admin.register(AnalyticsSnapshot)
class AnalyticsSnapshotAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(CategoryAnalytics)
class CategoryAnalyticsAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

@admin.register(MediatorPerformanceMetric)
class MediatorPerformanceMetricAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ()

