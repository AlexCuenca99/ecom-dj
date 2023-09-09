from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category
from .serializers import ParentCategorySerializer
from .utils import parent_category_setter, parent_category_setter_retrieve


class ParentCategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)
    permission_classes = [AllowAny]
    serializer_class = ParentCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id"]

    def list(self, request, *args, **kwargs):
        data = parent_category_setter(self.get_queryset())
        serializer = self.get_serializer(instance=data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ParentCategoryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ParentCategorySerializer

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()

        data = parent_category_setter_retrieve(category)

        serializer = self.get_serializer(instance=data)

        return Response(serializer.data, status=status.HTTP_200_OK)
