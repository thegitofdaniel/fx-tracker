# Generated by Django 4.0.4 on 2022-04-29 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='summary',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
