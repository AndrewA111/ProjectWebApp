# Generated by Django 2.1.5 on 2020-08-13 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0012_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
