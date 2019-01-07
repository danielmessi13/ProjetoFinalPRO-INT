# Generated by Django 2.1.4 on 2019-01-06 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0022_auto_20190106_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bloqueio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bloqueado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bloqueios_feitos', to='social.Usuario')),
                ('bloqueador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bloqueios_recebidos', to='social.Usuario')),
            ],
        ),
    ]
