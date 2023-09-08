from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "compare_price", "stock", "sold")
    list_display_links = ("id", "name")
    list_filter = ("category",)
    list_editable = (
        "price",
        "compare_price",
        "stock",
    )
    search_fields = ("name",)
    list_per_page = 25


admin.site.register(Product, ProductAdmin)
