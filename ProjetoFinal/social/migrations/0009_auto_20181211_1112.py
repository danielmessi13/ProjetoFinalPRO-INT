# Generated by Django 2.1.3 on 2018-12-11 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0008_auto_20181211_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='criador',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='criador', to='social.Usuario'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='descricao',
            field=models.TextField(default='Sem descrição'),
        ),
    ]
