from django.urls import path, include
from rest_framework.routers import DefaultRouter

import apps.loader.views


router = DefaultRouter()
router.register("bookmark", apps.loader.views.BookmarkViewSet, basename="bookmark")

urlpatterns = [
    path("", include(router.urls)),
]
