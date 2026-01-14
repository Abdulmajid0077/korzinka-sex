from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission)
from django.contrib.auth.models import User




class UserManager(BaseUserManager):
    def create_user(self, username, phone, password=None):
        if not username:
            raise ValueError("Username majburiy")
        if not phone:
            raise ValueError("Telefon raqam majburiy")
        if not password:
            raise ValueError("Parol majburiy")

        user = self.model(
            username=username,
            phone=phone,
        )
        user.set_password(password)
        user.is_active = False  
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone, password):
        user = self.create_user(username, phone, password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.korzinka = True
        user.seriyo = True
        user.salfetka = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=15, unique=True)

    korzinka = models.BooleanField(default=False)
    seriyo = models.BooleanField(default=False)
    salfetka = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']

   
    groups = models.ManyToManyField(
        Group,
        related_name='api_user_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='api_user_permissions_set', 
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username

