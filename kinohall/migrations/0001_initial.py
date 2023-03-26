# Generated by Django 4.1.5 on 2023-03-26 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('seats', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('year', models.PositiveIntegerField()),
                ('image', models.ImageField(blank=True, upload_to='products/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kinohall.hall')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kinohall.movie')),
            ],
        ),
    ]