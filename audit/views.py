from django.shortcuts import render
from .models import RequestLog

def recent_requests(request):
    logs = RequestLog.objects.all()[:10]
    return render(request, 'audit/request_logs.html', {'logs': logs})