from rest_framework import routers

from .viewsets import CartModelViewSet

router = routers.DefaultRouter()

router.register(r"carts", CartModelViewSet, basename="carts")
