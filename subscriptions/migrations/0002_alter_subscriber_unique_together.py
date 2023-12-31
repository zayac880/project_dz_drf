# Generated by Django 4.2.5 on 2023-10-04 13:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0005_course_owner_lesson_owner'),
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subscriber',
            unique_together={('user', 'course')},
        ),
    ]
