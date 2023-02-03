from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from coolmarks import settings


@ensure_csrf_cookie
@require_http_methods(["GET"])
def status_view(request):
    return JsonResponse(
        {
            "debug": settings.DEBUG,
            "authenticated": request.user.is_authenticated,
        }
    )
