from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .serializers import ProductModelSerializer
from .utils.views_utils import get_related_products


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        "price": ["gte", "lte", "exact", "lt", "gt"],
        "category": ["exact"],
    }
    ordering_fields = ["price", "name", "created"]
    search_fields = [
        "name",
    ]

    @action(
        detail=True,
        methods=["get"],
        url_name="related-products",
        url_path="related-products",
        permission_classes=[IsAuthenticatedOrReadOnly],
    )
    def related_products(self, request, pk=None):
        product = self.get_object()

        related_products = get_related_products(product)
        serializer = self.get_serializer(instance=related_products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
