from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Category


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category
    authentication_classes = [IsAuthenticatedOrReadOnly]
