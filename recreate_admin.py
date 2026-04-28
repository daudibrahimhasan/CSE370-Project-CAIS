import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cais_project.settings')
django.setup()

User = get_user_model()

def recreate_admin():
    username = 'admin'
    password = 'admin123'
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username=username, password=password, email='admin@cais.gov.bd')
        user.role = 'Admin'
        user.save()
        print(f"User '{username}' created successfully.")
    else:
        print(f"User '{username}' already exists.")

if __name__ == "__main__":
    recreate_admin()
