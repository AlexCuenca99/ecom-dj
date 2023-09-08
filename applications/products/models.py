import uuid
from django.db import models
from django.contrib.auth import get_user_model

from model_utils.models import TimeStampedModel

from applications.categories.models import Category
from .utils.models_utils import product_photo_file_path

User = get_user_model()


class Product(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Name", max_length=255)
    sold = models.PositiveIntegerField("Sold", default=0)
    stock = models.PositiveIntegerField("Stock", default=0)
    photo = models.ImageField("Photo", upload_to=product_photo_file_path)
    description = models.TextField("Description", max_length=255)
    is_available = models.BooleanField("Is available", default=True)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    compare_price = models.DecimalField(
        "Compare price", max_digits=10, decimal_places=2
    )
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name + " - " + str(self.price) + " $"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created"]
        unique_together = ["name", "owner"]
