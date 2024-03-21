from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from api.views import (RecipesViewSet, CustomUserViewSet, TagViewSet,
                       IngredientViewSet)

router_v1 = routers.DefaultRouter()

router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register(r'recipes', RecipesViewSet, basename='recipes')

router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    # Создание и удаление токена.
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'', include(router_v1.urls)),
]
