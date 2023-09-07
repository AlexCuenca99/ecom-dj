from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .serializers import ProductModelSerializer


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {"name": ["exact"], "price": ["gte", "lte", "exact", "lt", "gt"]}
    ordering_fields = ["price", "name"]
    search_fields = [
        "name",
    ]
