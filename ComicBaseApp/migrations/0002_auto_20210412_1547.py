# Generated by Django 3.1.7 on 2021-04-12 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ComicBaseApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comicbook',
            name='image',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='comicbook',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comicbook',
            name='published_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comicbook',
            name='publisher',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='comicbook',
            name='volume',
            field=models.CharField(max_length=150),
        ),
    ]
