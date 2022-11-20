from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("api/", include("apps.urls")),
    path("api/auth/", include("rest_framework.urls")),
    path("_/vip/", admin.site.urls),
]
