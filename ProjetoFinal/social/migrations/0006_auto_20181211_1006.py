# Generated by Django 2.1.3 on 2018-12-11 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0005_auto_20181211_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='usuarios',
            field=models.ManyToManyField(null=True, related_name='grupo_usuario', to='social.Usuario'),
        ),
    ]