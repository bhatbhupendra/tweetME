# Generated by Django 3.0.8 on 2020-07-20 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_auto_20200720_1519'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweets',
            old_name='profile',
            new_name='profileUser',
        ),
    ]
