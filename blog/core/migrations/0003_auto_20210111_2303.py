# Generated by Django 3.1.4 on 2021-01-11 23:03

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210107_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumb',
            field=models.ImageField(default='teste', upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
