# Generated by Django 2.2.12 on 2021-08-19 21:18

from django.db import migrations, models
import myblog.models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0011_auto_20210819_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to=myblog.models.get_uploud_path, verbose_name='Image'),
        ),
    ]
