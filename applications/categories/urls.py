from django.urls import include, path

from .routers import router
from .views import ParentCategoryListAPIView

app_name = "categories_app"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "parent-categories/",
        ParentCategoryListAPIView.as_view(),
        name="parent-categories",
    ),
]
