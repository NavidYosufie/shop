from django.utils.crypto import get_random_string
from PIL import Image
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError('Users must have an email address')

        user = self.model(
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        """
        Creates and saves a superuser with the given email, and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    image_profile = models.ImageField(null=True, blank=True)
    username = models.CharField(max_length=50, unique=True, null=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(unique=True, null=True, max_length=11)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def str(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app app_label?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Otp(models.Model):
    token = models.CharField(max_length=32, null=True)
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    expiation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    phone = models.CharField(max_length=11)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=300)
    full_name = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=16)

    def __str__(self):
        return self.address


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='profile-avatar')

    def __str__(self):
        return self.user.username

    # def save(self, *args, **kwargs):
    #     # save the profile first
    #     super().save(*args, **kwargs)
    #
    #     # resize the image
    #     img = Image.open(self.image.path)
    #     output_size = (500, 500)
    #     # create a thumbnail
    #     img.thumbnail(output_size)
    #     # overwrite the larger image
    #     img.save(self.image.path)
