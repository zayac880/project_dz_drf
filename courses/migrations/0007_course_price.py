# Generated by Django 4.2.5 on 2023-10-12 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_alter_payment_pay_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.IntegerField(default=0, verbose_name='цена'),
            preserve_default=False,
        ),
    ]
