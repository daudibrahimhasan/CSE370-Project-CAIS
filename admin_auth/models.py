from django.db import models
from django.contrib.auth.models import AbstractUser

# We are extending AbstractUser to add 'role' or any other specific needed fields, though built-in user logic handles much of admin.
class AdminUser(AbstractUser):
    # AbstractUser already has username, password, email, first_name, last_name, is_staff, is_superuser, is_active
    ROLE_CHOICES = [
        ('Admin', 'Administrator'),
        ('Viewer', 'Viewer'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Viewer')

    # To avoid clashes with built-in auth.User since we didn't set AUTH_USER_MODEL right away
    # We will use this as a proxy or just setup AUTH_USER_MODEL 
    pass
