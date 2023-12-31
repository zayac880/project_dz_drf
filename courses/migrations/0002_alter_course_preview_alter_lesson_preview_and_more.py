# Generated by Django 4.2.5 on 2023-09-13 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='course_previews/', verbose_name='превью'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='lesson_previews/', verbose_name='превью'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='video_link',
            field=models.URLField(blank=True, null=True, verbose_name='ссылка на видео'),
        ),
    ]
