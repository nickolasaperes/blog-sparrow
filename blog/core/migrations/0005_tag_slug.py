# Generated by Django 3.1.4 on 2021-01-28 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210123_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default='slug'),
            preserve_default=False,
        ),
    ]