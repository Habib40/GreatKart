# Generated by Django 5.0.1 on 2024-10-16 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0007_alter_cart_cart_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(blank=True, default='6774959a-b03a-4ce8-a6ae-604edbbb608d', max_length=250),
        ),
    ]
