from typing import List
from dataclasses import dataclass
from django.db.models.query import QuerySet

from .models import Category


from django.db.models import Prefetch


@dataclass
class ParentCategory:
    id: str
    name: str
    children: list


def parent_category_setter(categories: QuerySet[Category]) -> QuerySet[Category]:
    """Generate a query for set categories"""

    children = Category.objects.filter(parent__in=categories)

    formatted_parent_categories = categories.prefetch_related(
        Prefetch("category_set", queryset=children, to_attr="children")
    )

    return formatted_parent_categories


def parent_category_setter_retrieve(category: Category) -> ParentCategory:
    """Generate a query for the requested category"""

    category_entry = ParentCategory(
        id=str(category.id), name=category.name, children=category.category_set.all()
    )

    return category_entry
