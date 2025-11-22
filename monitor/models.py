from django.db import models


class ApiEndpoint(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name


class HealthCheck(models.Model):
    url = models.URLField()
    status_code = models.IntegerField(null=True, blank=True)
    is_up = models.BooleanField(default=False)
    response_time_ms = models.FloatField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "UP" if self.is_up else "DOWN"
        return f"{self.url} - {status}"
