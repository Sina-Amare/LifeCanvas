from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Override email to make it required and unique
    email = models.EmailField(unique=True, blank=False, null=False)
    # Add custom fields
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Specify the field to use for authentication (instead of username)
    USERNAME_FIELD = 'email'
    # Fields required when creating a user via createsuperuser
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
