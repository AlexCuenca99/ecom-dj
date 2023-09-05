from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Category
from .serializers import CategoryModelSerializer


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
