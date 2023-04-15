from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from api.views import RecipesViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'recipes', RecipesViewSet)

urlpatterns = [
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'', include(router_v1.urls)),

]
