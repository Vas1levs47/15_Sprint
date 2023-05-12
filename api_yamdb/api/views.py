from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from api.filter import TitleFilterSet
from api.permissions import AdminOrReadOnly, AuthorModerOrRead
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleEditSerializer, TitleViewSerializer)
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    """Ресурс categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   mixins.ListModelMixin, viewsets.GenericViewSet):
    """Ресурс genres."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Ресурс titles."""
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        """Несколько serializer_class."""
        if self.action == 'list' or self.action == 'retrieve':
            return TitleViewSerializer
        return TitleEditSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """Ресурс reviews."""
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModerOrRead,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(title_id=self.get_title().id, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Ресурс comments."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorModerOrRead,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            title_id=self.get_title().id,
            review_id=self.get_review().id, author=self.request.user)
