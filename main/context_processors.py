from django.conf import settings

def settings_context(request):
    safe_settings = {
        'DEBUG': settings.DEBUG,
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'TIME_ZONE': settings.TIME_ZONE,
        'INSTALLED_APPS': settings.INSTALLED_APPS,
        'DATABASES': {
            'default': {
                'ENGINE': settings.DATABASES['default']['ENGINE'],
                'NAME': settings.DATABASES['default']['NAME'],
            }
        }
    }
    return {'settings': safe_settings}