# Generated by Django 5.1.1 on 2024-09-28 19:36

import CorralSnake.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_pfp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pfp',
            field=models.ImageField(default='defaults/pfps/default.png', upload_to=CorralSnake.utils.uuid_upload_to),
        ),
    ]
