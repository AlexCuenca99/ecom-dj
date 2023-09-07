from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Product
from .serializers import ProductModelSerializer


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
