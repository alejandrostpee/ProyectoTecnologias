# Generated by Django 5.0.2 on 2025-05-21 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud_escolar_api', '0006_rename_tipo_evento_evento_tipo_evento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evento',
            old_name='Fecha_realización',
            new_name='fecha_evento',
        ),
    ]
