# Generated by Django 2.2.3 on 2019-08-06 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_auto_20190807_0200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='desc',
            new_name='description',
        ),
    ]
