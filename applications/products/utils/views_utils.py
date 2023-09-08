from django.db.models import QuerySet
from applications.products.models import Product


def get_related_products(product: Product) -> QuerySet[Product]:
    if product.category_parent:
        print("Producto category has parent")
    else:
        print("Producto category has no parent")

    return Product.objects.exclude(id=product.id).filter(
        category=product.category, is_available=True
    )
