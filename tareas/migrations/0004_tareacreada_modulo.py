# Generated by Django 5.1.6 on 2025-02-26 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0003_tareadelalumno_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='tareacreada',
            name='modulo',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
