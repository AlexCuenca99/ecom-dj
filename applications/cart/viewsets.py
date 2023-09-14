from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Cart
from .serializers import CartModelSerializer


class CartModelViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
