# Generated by Django 5.1.2 on 2024-10-24 15:58

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editors_choice', '0002_editorchoice_week_remove_editorchoice_food_items_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodrecommendation',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]