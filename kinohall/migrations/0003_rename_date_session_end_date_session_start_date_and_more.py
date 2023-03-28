# Generated by Django 4.1.5 on 2023-03-27 12:37

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kinohall', '0002_alter_movie_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='date',
            new_name='end_date',
        ),
        migrations.AddField(
            model_name='session',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='hall',
            name='seats',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(20), django.core.validators.MaxValueValidator(250)]),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(2030)]),
        ),
    ]