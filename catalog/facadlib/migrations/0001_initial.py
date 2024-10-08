# Generated by Django 5.1 on 2024-08-13 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_id', models.IntegerField()),
                ('ad_id', models.IntegerField()),
                ('text', models.TextField()),
                ('link', models.URLField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
