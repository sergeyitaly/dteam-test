import json
from .models import RequestLog
from django.contrib.auth import get_user_model

User = get_user_model()

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip logging for admin and static files
        if request.path.startswith(('/admin', '/static')):
            return self.get_response(request)

        response = self.get_response(request)

        try:
            user = request.user if request.user.is_authenticated else None
            query_params = dict(request.GET) if request.GET else None

            RequestLog.objects.create(
                method=request.method,
                path=request.path,
                query_params=query_params,
                ip_address=self.get_client_ip(request),
                user=user,
                response_code=response.status_code
            )
        except Exception as e:
            # Don't break the request if logging fails
            pass

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip