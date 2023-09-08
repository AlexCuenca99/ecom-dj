import os


# Set article photo path
def product_photo_file_path(instance, filename) -> str:
    ext = filename.split(".")[-1]
    filename = "product_photo_{}.{}".format(instance.id, ext)

    return os.path.join(
        "accounts", "user_%s" % instance.owner.pk, "images", "products", filename
    )
