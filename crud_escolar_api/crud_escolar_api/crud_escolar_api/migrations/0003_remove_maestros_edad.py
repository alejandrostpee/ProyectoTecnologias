# Generated by Django 5.0.2 on 2025-03-16 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud_escolar_api', '0002_administradores_alumnos_maestros_delete_profiles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maestros',
            name='edad',
        ),
    ]
