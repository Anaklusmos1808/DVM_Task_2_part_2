# Generated by Django 4.1.3 on 2023-01-26 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuizMania', '0004_truefalseanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='truefalseanswer',
            name='option_1',
            field=models.CharField(default='True', editable=False, max_length=100),
        ),
        migrations.AddField(
            model_name='truefalseanswer',
            name='option_2',
            field=models.CharField(default='False', editable=False, max_length=100),
        ),
    ]
