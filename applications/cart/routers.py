from rest_framework import routers

from .viewsets import CartModelViewSet, CartItemModelViewSet

router = routers.DefaultRouter()

router.register(r"carts/<str:pk>/items", CartItemModelViewSet, basename="carts-items")
router.register(r"carts", CartModelViewSet, basename="carts")
