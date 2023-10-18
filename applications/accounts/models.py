import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from model_utils.models import TimeStampedModel

from .managers import CustomUserManager
from .choices import GENDER_CHOICES
from .utils import photo_file_name, set_age


class CustomUser(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    age = models.PositiveSmallIntegerField("Age")
    address = models.CharField("Address", max_length=100, blank=True)
    phone = models.CharField("Phone", max_length=20, blank=True)
    last_name = models.CharField("Last Name", max_length=100)
    first_name = models.CharField("First Name", max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField("Email", max_length=100, unique=True)
    username = models.CharField("Username", max_length=100, unique=True)
    birth = models.DateField("Birth", auto_now=False, auto_now_add=False)
    gender = models.CharField("Gender", choices=GENDER_CHOICES, max_length=10)
    photo = models.ImageField(
        "Profile photo",
        upload_to=photo_file_name,
        default="accounts/default/images/profile/no-user-photo.png",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
        "birth",
        "gender",
        "photo",
    ]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.age = set_age(self.birth)
        super().save(*args, **kwargs)

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    @property
    def cart_id(self):
        return self.cart.id

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"

    def set_age(self, birth):
        self.age = set_age(birth)
