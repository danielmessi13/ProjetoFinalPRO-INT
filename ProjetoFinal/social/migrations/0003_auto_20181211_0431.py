# Generated by Django 2.1.3 on 2018-12-11 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20181211_0421'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postagem',
            options={'ordering': ['-data']},
        ),
    ]
