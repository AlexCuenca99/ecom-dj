import os
from datetime import datetime
from django.conf import settings

from .models import Product


# Set article photo path
def product_photo_file_path(instance: Product, filename) -> str:
    ext = filename.split(".")[-1]
    filename = "product_photo_{}.{}".format(instance.id, ext)

    return os.path.join(
        "accounts", "user_%s" % instance.owner.pk, "images", "products", filename
    )
