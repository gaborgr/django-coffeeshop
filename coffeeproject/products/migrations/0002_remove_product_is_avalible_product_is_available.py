# Generated by Django 5.2.3 on 2025-06-22 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_avalible',
        ),
        migrations.AddField(
            model_name='product',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='Available?'),
        ),
    ]
