# Generated by Django 5.1 on 2024-10-26 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards_makanan', '0007_merge_0005_makanan_0006_auto_20241026_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
    ]
