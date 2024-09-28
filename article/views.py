from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from user.permissions import TeacherOnly
from .serializers import ArticleSerializer

User = get_user_model()


class ArticleViewSet(viewsets.ModelViewSet):
    lookup_field = 'public_id'
    queryset = User.objects.all().order_by('id')
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        """
        Creates a new article. Only accessible by users with the 'TeacherOnly' permission.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves an article by its public ID. Any authenticated user can access this.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        Lists all articles. Only accessible by authenticated users.
        """
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing article. Only the author of the article is allowed to update it.
        """
        article = self.get_object()
        if article.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(article, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates an existing article. Only the author of the article is allowed to make changes.
        """
        article = self.get_object()
        if article.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes an article. Only the author of the article is allowed to delete it.
        """
        article = self.get_object()
        if article.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        self.perform_destroy(article)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [TeacherOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
