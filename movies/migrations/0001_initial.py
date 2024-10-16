# Generated by Django 5.1.2 on 2024-10-14 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('director', models.CharField(max_length=255)),
                ('imdb_rating', models.FloatField()),
                ('description', models.TextField()),
                ('poster', models.ImageField(blank=True, null=True, upload_to='movies/posters/')),
            ],
        ),
    ]
