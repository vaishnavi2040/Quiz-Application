# Generated by Django 4.1 on 2022-10-12 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0005_remove_question_difficulty_remove_question_subject_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]