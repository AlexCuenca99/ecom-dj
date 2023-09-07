from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Category
from .serializers import ParentCategorySerializer
from .utils import parent_category_setter, parent_category_setter_retrieve


class ParentCategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)
    permission_classes = [AllowAny]
    serializer_class = ParentCategorySerializer

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
