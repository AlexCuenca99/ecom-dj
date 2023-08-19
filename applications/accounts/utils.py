import os
from datetime import datetime
from django.conf import settings


# Calculate age based on birth date of the user
def set_age(birth) -> int:
    current_date = datetime.now()
    birth = datetime.strptime(str(birth), "%Y-%m-%d")

    age = current_date.year - birth.year

    # Verify if not have yet completed years
    if current_date.month < birth.month or (
        current_date.month == birth.month and current_date.day < birth.day
    ):
        age -= 1

    return age


# Define the path of the photo file
def photo_file_name(instance, filename) -> str:
    ext = filename.split(".")[-1]
    filename = "photo_{}.{}".format(instance.id, ext)

    return os.path.join(
        "accounts", "user_%s" % instance.id, "images", "profile", filename
    )
