# Generated by Django 2.2.3 on 2019-07-16 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20190716_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
