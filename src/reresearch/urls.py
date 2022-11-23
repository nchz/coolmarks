from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path("", TemplateView.as_view(template_name="main.html")),
    path("api/", include("apps.urls")),
    # path("api/auth/", include("rest_framework.urls")),
    path("api/auth/", include("allauth.urls")),
    path("_/vip/", admin.site.urls),
]
