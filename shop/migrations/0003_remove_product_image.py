# Generated by Django 5.1.3 on 2024-11-21 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]