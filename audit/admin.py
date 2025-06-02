from django.contrib import admin
from .models import RequestLog

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'method', 'path', 'response_code', 'user')
    list_filter = ('method', 'response_code')
    search_fields = ('path', 'user__username')