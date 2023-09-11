from uuid import UUID

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

    def get_queryset(self):
        categories_ids_params = self.request.query_params.get("id", None)

        # Comprobar que categories_ids_params se halle en la peticion
        if categories_ids_params is not None:
            try:
                # Separar los ids de las categorias
                categories_ids = categories_ids_params.split(",")

                for category_id in categories_ids:
                    category_id = UUID(category_id)

                queryset = parent_category_setter(
                    Category.objects.filter(parent=None, id__in=categories_ids)
                )
                return queryset
            except:
                return []
        else:
            queryset = parent_category_setter(super().get_queryset())
            return queryset

    def list(self, request, *args, **kwargs):
        data = self.get_queryset()

        if len(data) != 0:
            serializer = self.get_serializer(instance=data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            response = {"detail": "At least one id was not found"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ParentCategoryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ParentCategorySerializer

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()

        data = parent_category_setter_retrieve(category)

        serializer = self.get_serializer(instance=data)

        return Response(serializer.data, status=status.HTTP_200_OK)
