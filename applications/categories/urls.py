from django.urls import include, path

from .routers import router
from .views import ParentCategoryListAPIView, ParentCategoryRetrieveAPIView

app_name = "categories_app"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "categories/parents",
        ParentCategoryListAPIView.as_view(),
        name="categories-parents-list",
    ),
    path(
        "categories/parents/<pk>",
        ParentCategoryRetrieveAPIView.as_view(),
        name="categories-parents-detail",
    ),
]
