import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from api.utils.regexp import match_pattern
from cloudinary.models import CloudinaryField
import cloudinary
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, phone_number, location=None, user_currency=None):
        password_pattern = r"^(?=.*[A-Za-z])(?=.*[@$!%*#?&_])[\w@$!%*#?&_]{8,150}$"

        if not username or not match_pattern(r'^[\w\d_-]{3,150}$', username):
            raise ValueError('Username field required')
        if not email:
            raise ValueError('Email field required')
        if not password or not match_pattern(password_pattern, password):
            raise ValueError('Password field required')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            location=location,
            user_currency=user_currency,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.model(
            username=username,
            # email=self.normalize_email(email),
            is_staff=True,
            is_superuser=True
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    first_name = models.CharField(null=True, blank=True, max_length=255)
    last_name = models.CharField(null=True, blank=True, max_length=255)
    location = models.CharField(max_length=150, null=True, blank=True)
    user_currency = models.CharField(
        max_length=5, null=True, blank=True, default='Q')
    objects = UserManager()
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'


class UserContactInformation(models.Model):
    user = models.ForeignKey(
        User, related_name="user_contact_information", on_delete=models.CASCADE)
    contact_type = models.CharField(max_length=150)
    contact = models.CharField(max_length=255)


class ProductTags(models.Model):
    name = models.CharField(max_length=150)


class Product(models.Model):
    user = models.ForeignKey(User, related_name="user",
                             on_delete=models.CASCADE)
    tags = models.ManyToManyField(ProductTags, related_name="tags")
    name = models.CharField(max_length=150)
    description = models.TextField()
    aproximate_price = models.FloatField()
    last_update = models.DateTimeField(auto_now=True)
    possible_interchanges = models.TextField()
    in_revision = models.BooleanField(default=False)

    class Meta:
        ordering = ('last_update',)


class ProductReport(models.Model):
    report_from = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product")
    report_reason = models.TextField(max_length=700, default="Is not")


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="product_image", on_delete=models.CASCADE)
    # image = models.ImageField(upload_to="product-images")
    image = CloudinaryField("image", folder="swap-it/product-images") 

    @staticmethod
    def delete_image(obj):
        cloudinary.uploader.destroy(obj.image.public_id,invalidate=True)
        obj.delete()

class ConfirmationCode(models.Model):
    username = models.CharField(unique=True, max_length=150)
    code = models.CharField(max_length=4)
