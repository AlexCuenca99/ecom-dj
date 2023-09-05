from django.urls import include, path

from .routers import router

app_name = "categories_app"

urlpatterns = [
    path("", include(router.urls)),
]
