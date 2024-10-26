# cards_makanan/migrations/0002_create_admin_user.py
from django.db import migrations

def create_admin_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username='admin').exists():
        User.objects.create_user(
            username='admin',
            email='admin@gmail.com',
            password='halal123',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

def remove_admin_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='admin').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('cards_makanan', '0005_makanan'),
    ]

    operations = [
        migrations.RunPython(create_admin_user, remove_admin_user),
    ]
