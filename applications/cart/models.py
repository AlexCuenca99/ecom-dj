import uuid
from django.db import models, transaction
from django.dispatch import receiver
from django.db.models.signals import post_save

from model_utils.models import TimeStampedModel

from applications.products.models import Product, User


class Cart(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    products = models.ManyToManyField(
        Product, through="CartItem", related_name="in_carts"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_items = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ["-created"]
        unique_together = ["user"]

    def __str__(self):
        return f"Cart - {self.user.username}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.update_totals()
            super().save(*args, **kwargs)

    def update_totals(self):
        cart_items = self.items.all()

        total_items = cart_items.count()
        total_price = sum(cart_item.partial_price for cart_item in cart_items)

        self.total_items = total_items
        self.total_price = total_price


class CartItem(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="in_cart"
    )
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        ordering = ["-created"]
        unique_together = ["cart", "product"]

    @property
    def partial_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.name} - {self.quantity} - {self.partial_price} $"


# This is not the best way to do the shopping cart creation but for the sake of
# the Django Signals learning is done this way
@receiver(post_save, sender=User, dispatch_uid="create_cart_user")
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
