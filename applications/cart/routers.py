from rest_framework import routers

from .viewsets import CartModelViewSet, CartItemModelViewSet

router = routers.DefaultRouter()

router.register(r"carts", CartModelViewSet, basename="carts")
router.register(
    r"carts/(?P<id>[^/.]+)/items", CartItemModelViewSet, basename="carts-items"
)
