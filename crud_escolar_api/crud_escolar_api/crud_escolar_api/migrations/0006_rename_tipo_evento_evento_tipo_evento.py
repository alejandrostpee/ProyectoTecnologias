# Generated by Django 5.0.2 on 2025-05-21 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud_escolar_api', '0005_evento_cupo_máximo_evento_descripción_breve_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evento',
            old_name='Tipo_evento',
            new_name='tipo_evento',
        ),
    ]
