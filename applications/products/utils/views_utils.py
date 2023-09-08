from django.db.models import QuerySet

from ..models import Product
from applications.categories.models import Category


def get_related_products(product: Product) -> QuerySet[Product]:
    # Si el producto tiene categoria padre
    if product.category.parent:
        # Obtener categorias hijas
        related_categories = product.category.parent.category_set.all()

        # Obtener productos de las categorias hijas y excluir el producto actual
        related_products = Product.objects.filter(
            category__in=related_categories
        ).exclude(id=product.id)

    # Si el producto no tiene categoria padre
    else:
        # Obtener productos de la misma categoria padre y excluir el producto actual
        related_products = Product.objects.filter(category=product.category).exclude(
            id=product.id
        )

    return related_products
