from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Category
from .serializers import ParentCategorySerializer
from .utils import parent_category_setter


class ParentCategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ParentCategorySerializer

    def get(self, request, *args, **kwargs):
        data = parent_category_setter()
        serializer = self.get_serializer(instance=data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
