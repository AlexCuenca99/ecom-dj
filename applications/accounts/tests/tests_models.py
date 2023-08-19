from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import CustomUser
from ..utils import set_age, photo_file_name


class CreateSingleUserTest(TestCase):
    """Test module for CustomUser model"""

    def setUp(self) -> None:
        """Set up a method which is used to initialize beofer any test run"""
        self.super_user_info = self.generate_super_user_info()
        self.user_info = self.generate_user_info()
        self.user_no_photo_info = self.generate_user_no_photo_info()
        self.image = self.generate_image()

    def generate_image(self):
        return SimpleUploadedFile(
            "test_image.png", b"dummy_content", content_type="image/jpeg"
        )

    def generate_super_user_info(self):
        return {
            "email": "admin@admin.com",
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "is_staff": True,
            "is_admin": True,
            "is_active": True,
            "phone": "0989181061",
            "gender": "M",
            "photo": self.generate_image(),
        }

    def generate_user_info(self):
        return {
            "email": "admin@admin.com",
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "phone": "0989181061",
            "gender": "F",
            "photo": self.generate_image(),
        }

    def generate_user_no_photo_info(self):
        return {
            "email": "admin@admin.com",
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "phone": "0989181061",
            "gender": "F",
        }

    def test_create_superuser(self):
        """Test for create a superuser"""
        superuser = CustomUser.objects.create(**self.super_user_info)

        self.assertEqual(superuser.email, self.super_user_info["email"])
        self.assertEqual(superuser.phone, self.super_user_info["phone"])
        self.assertEqual(superuser.birth, self.super_user_info["birth"])
        self.assertEqual(superuser.age, set_age(self.super_user_info["birth"]))
        self.assertEqual(superuser.gender, self.super_user_info["gender"])
        self.assertEqual(superuser.address, self.super_user_info["address"])
        self.assertEqual(superuser.is_staff, self.super_user_info["is_staff"])
        self.assertEqual(superuser.is_admin, self.super_user_info["is_admin"])
        self.assertEqual(superuser.last_name, self.super_user_info["last_name"])
        self.assertEqual(superuser.is_active, self.super_user_info["is_active"])
        self.assertEqual(superuser.first_name, self.super_user_info["first_name"])
        self.assertEqual(
            superuser.photo.name,
            photo_file_name(superuser, filename=self.super_user_info["photo"].name),
        )
