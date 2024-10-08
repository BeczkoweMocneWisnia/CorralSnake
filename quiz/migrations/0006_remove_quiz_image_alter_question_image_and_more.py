# Generated by Django 5.1.1 on 2024-09-29 04:45

import CorralSnake.utils
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_alter_question_image_alter_quiz_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='image',
        ),
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(null=True, upload_to=CorralSnake.utils.uuid_upload_to),
        ),
        migrations.AlterField(
            model_name='questionanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='possible_answers', to='quiz.question'),
        ),
    ]
