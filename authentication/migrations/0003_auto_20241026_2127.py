from django.db import migrations
from django.contrib.auth.models import User

def create_admin_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='halal123'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_userprofile_bio'),  
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]
