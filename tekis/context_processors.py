from django.conf import settings

def site(request):
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_URL": settings.SITE_URL,
        "BASE_TEMPLATE": settings.BASE_TEMPLATE
    }
