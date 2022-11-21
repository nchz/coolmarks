from rest_framework import viewsets, permissions

from apps.loader.models import Bookmark, BookmarkSerializer


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]
    template_name = "loader/bookmark.html"

    def get_queryset(self):
        queryset = Bookmark.objects.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
