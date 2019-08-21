# Generated by Django 2.2.3 on 2019-07-21 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20190716_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='is_ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Product')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Profile')),
            ],
            options={
                'verbose_name': 'Wishlist',
            },
        ),
    ]
