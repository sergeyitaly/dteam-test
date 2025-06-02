from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')
        if not request.user.is_staff:
            return HttpResponseForbidden("403 Forbidden")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
