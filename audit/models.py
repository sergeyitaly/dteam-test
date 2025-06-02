from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    query_params = models.JSONField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True)
    user = models.ForeignKey(
        User, 
        null=True, 
        on_delete=models.SET_NULL
    )
    response_code = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Request Log'
        verbose_name_plural = 'Request Logs'

    def __str__(self):
        return f"{self.method} {self.path} ({self.response_code})"