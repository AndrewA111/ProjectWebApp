# Generated by Django 2.1.5 on 2020-08-10 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0009_auto_20200810_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='testFile',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]