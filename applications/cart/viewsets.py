from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS

from .models import Cart
from .serializers import CartModelSerializer


class CartModelViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]
