# Generated by Django 5.0.1 on 2024-10-14 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_alter_cart_cart_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(blank=True, default='7ad42f92-c1dd-41cc-bf09-0802edadc1da', max_length=250),
        ),
    ]
