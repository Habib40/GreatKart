# Generated by Django 5.0.1 on 2024-10-13 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(blank=True, default='081b87a5-5ff5-4f94-a7d9-134bf4511c35', max_length=250),
        ),
    ]