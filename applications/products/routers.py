from rest_framework import routers

from .viewsets import ProductModelViewSet


router = routers.DefaultRouter()

router.register(r"products", ProductModelViewSet, basename="products")
