from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsOwnerOrReadOnly
from api.serializers import RecipeListSerializer, RecipeCreateUpdateSerializer
from recipes.models import Recipe


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', ]
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateUpdateSerializer

        return RecipeListSerializer

    def get_queryset(self):
        qs = Recipe.objects.add_user_annotations(self.request.user.pk)

        # Фильтры из GET-параметров запроса, например.
        author = self.request.query_params.get('author', None)
        if author:
            qs = qs.filter(author=author)

        return qs
