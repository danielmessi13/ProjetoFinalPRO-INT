# Generated by Django 2.2a1 on 2019-01-25 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0026_auto_20190125_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='foto',
            field=models.ImageField(default='img/user.png', upload_to='profiles'),
        ),
    ]
