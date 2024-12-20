# Generated by Django 5.1.2 on 2024-10-24 15:55

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='food_type',
            field=models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('souvenirs', 'Souvenirs')], default='lunch', max_length=9),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='description',
            field=models.TextField(default='No description available.'),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
