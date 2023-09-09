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


def get_related_products_by_category(category_id: str) -> QuerySet[Product]:
    category = Category.objects.get(id=category_id)

    # Si la categoria tiene categoria padre
    if category.parent:
        # Obtener productos de la misma categoria padre y excluir el producto actual
        related_products = Product.objects.filter(category=category)

    # Si la categoria no tiene categoria padre
    else:
        # Obtener categorias hijas
        related_categories = category.category_set.all()

        # Obtener productos de las categorias hijas
        related_products = Product.objects.filter(category__in=related_categories)

    return related_products
