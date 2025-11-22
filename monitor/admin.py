from django.contrib import admin
from .models import ApiEndpoint, HealthCheck


@admin.register(ApiEndpoint)
class ApiEndpointAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(HealthCheck)
class HealthCheckAdmin(admin.ModelAdmin):
    list_display = ("url", "status_code", "is_up", "checked_at")
    list_filter = ("is_up", "checked_at")
