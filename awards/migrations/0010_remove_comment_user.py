# Generated by Django 3.1.2 on 2020-10-26 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0009_auto_20201026_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
    ]
