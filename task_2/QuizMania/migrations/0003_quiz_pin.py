# Generated by Django 4.1.3 on 2023-01-25 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuizMania', '0002_quiz_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='pin',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]