# Generated by Django 3.1.1 on 2020-12-30 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hms', '0003_auto_20201230_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='avatar',
            field=models.ImageField(blank=True, default='static/no-img.jpg', null=True, upload_to=''),
        ),
    ]
