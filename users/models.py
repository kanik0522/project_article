from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,Permission
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, username,email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Handles password hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_journalist', True)
        extra_fields.setdefault('is_editor', True)
        extra_fields.setdefault('is_head', True)
        extra_fields.setdefault('is_viewer', True)
        return self.create_user(username, email, password, **extra_fields)
    
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_journalist') is not True:
            raise ValueError('Superuser must have is_journalist=True.')
        if extra_fields.get('is_editor') is not True:
            raise ValueError('Superuser must have is_editor=True.')
        if extra_fields.get('is_head') is not True:
            raise ValueError('Superuser must have is_head=True.')
        
        return self.create_user(username, email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_journalist = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    is_head = models.BooleanField(default=False)  
    is_viewer = models.BooleanField(default=True)  
    objects = CustomUserManager()
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_superuser or self.user_permissions.filter(codename=perm).exists()

    def has_perms(self, perm_list):
        "Does the user have all permissions in perm_list?"
        return all(self.has_perm(perm) for perm in perm_list)

    def has_module_perms(self, app_label):
        "Does the user have permissions for the app `app_label`?"
        return self.is_superuser or self.user_permissions.filter(content_type__app_label=app_label).exists()

    def get_user_permissions(self, obj=None):
        "Return a set of permission strings that this user has."
        return set(self.user_permissions.values_list('codename', flat=True))

    def get_group_permissions(self, obj=None):
        "Return a set of permission strings that this user has through groups."
        return set(Permission.objects.filter(group__in=self.groups.all()).values_list('codename', flat=True))

    def get_all_permissions(self, obj=None):
        "Return a set of all permissions this user has."
        return self.get_user_permissions() | self.get_group_permissions()
    def set_password(self, raw_password):
        super().set_password(raw_password)

    def check_password(self, raw_password):
        return super().check_password(raw_password)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
    )

    class Meta:
        ordering = ['username']

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('journalist', 'Journalist'),
        ('editor', 'Editor'),
        ('head', 'Head'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='journalist')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()