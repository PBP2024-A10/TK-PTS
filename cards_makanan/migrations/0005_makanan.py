# Generated by Django 5.1.1 on 2024-10-25 14:29

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards_makanan', '0004_restaurant_menuitem_delete_makanan'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Makanan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama_makanan', models.CharField(max_length=100)),
                ('deskripsi_makanan', models.TextField()),
                ('kategori_makanan', models.CharField(max_length=50)),
                ('daftar_alergi', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
