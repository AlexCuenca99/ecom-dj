from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view


# Yasg Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="EcomDJ API",
        default_version="v1",
        description="API Docs for EcomDJ API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="alex-patricio1999@hotmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Base url's
    path("admin/", admin.site.urls),
    # Yasg urls'
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Djoser url's
    path("api/v1/", include("djoser.urls")),
    path("api/v1/", include("djoser.urls.jwt")),
    path("api/v1/", include("djoser.social.urls")),
    # Local apps url's
    path("api/v1/", include("applications.categories.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
