# Generated by Django 5.1.2 on 2024-12-21 12:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards_makanan', '0009_menuitem_image_url_menu'),
        ('editors_choice', '0010_foodcomment_author_uname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodrecommendation',
            name='food_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards_makanan.menuitem'),
        ),
    ]
