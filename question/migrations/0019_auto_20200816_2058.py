# Generated by Django 2.1.5 on 2020-08-16 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0018_auto_20200816_2055'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together={('name', 'course'), ('slug', 'course')},
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together={('name', 'lesson'), ('slug', 'lesson')},
        ),
    ]
