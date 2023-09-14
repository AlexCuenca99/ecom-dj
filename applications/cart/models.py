import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from model_utils.models import TimeStampedModel

from applications.products.models import Product, User


class Cart(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_items = models.PositiveSmallIntegerField(default=0)


class CartItem(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveSmallIntegerField(default=1)


@receiver(post_save, sender=User, dispatch_uid="create_cart_user")
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
