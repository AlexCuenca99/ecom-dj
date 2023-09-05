from rest_framework import routers

from .viewsets import CategoryModelViewSet

router = routers.DefaultRouter()

router.register(r"categories", CategoryModelViewSet, basename="categories")
