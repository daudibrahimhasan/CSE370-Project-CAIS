import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cais_project.settings')
django.setup()

User = get_user_model()

def reset_admin():
    username = 'admin'
    password = 'admin123'
    user, created = User.objects.get_or_create(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.role = 'Admin'
    user.save()
    print(f"User '{username}' password reset to '{password}'.")

if __name__ == "__main__":
    reset_admin()
