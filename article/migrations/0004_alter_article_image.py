# Generated by Django 5.1.1 on 2024-09-28 19:36

import CorralSnake.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_alter_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(null=True, upload_to=CorralSnake.utils.uuid_upload_to),
        ),
    ]
