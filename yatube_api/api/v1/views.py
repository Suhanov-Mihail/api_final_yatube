from django.shortcuts import get_object_or_404

from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .serializers import (CommentSerializer, FollowSerializer,
                          GroupSerializer, PostSerializer)
from .permissions import IsAuthorOrReadOnly

from posts.models import Follow, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    """Позволяет выполнять любые операции CRUD с моделью Post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Позволяет выполнять любые операции CRUD с моделью Comment"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Позволяет только получать данные модели Group"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FollowViewSet(viewsets.ModelViewSet):
    """Позволяет только получать данные модели Follow"""
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username', )
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
