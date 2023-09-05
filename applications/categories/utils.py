from dataclasses import dataclass

from .models import Category


@dataclass
class ParentCategory:
    id: str
    name: str
    children: list


def parent_category_setter() -> list[ParentCategory]:
    """Generate a query for set categories"""

    data = []

    categories = Category.objects.filter(parent=None)

    for category in categories:
        category_entry = ParentCategory(
            id=category.id, name=category.name, children=category.category_set.all()
        )
        data.append(category_entry)

    return data
