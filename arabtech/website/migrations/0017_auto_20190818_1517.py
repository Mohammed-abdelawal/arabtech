# Generated by Django 2.2.3 on 2019-08-18 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_invoice_done'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user_id',
            new_name='user',
        ),
    ]