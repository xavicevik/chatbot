# Generated by Django 3.0 on 2022-03-06 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0005_auto_20220306_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='conveniocda',
            name='revision',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='gestion.Fechasrevision'),
        ),
    ]
