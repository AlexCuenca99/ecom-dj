from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS

from .models import Cart
from .serializers import CartModelSerializer
from rest_framework.response import Response


class CartModelViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    def get_instance(self):
        return self.request.user.cart

    @action(
        detail=False,
        methods=["GET", "PATCH", "DELETE"],
        name="My cart",
        url_path="my-cart",
        url_name="my-cart",
    )
    def my_cart(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        if request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        if request.method == "DELETE":
            return Response(status=HTTP_200_OK)
