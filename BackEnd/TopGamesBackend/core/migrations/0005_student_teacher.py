# Generated by Django 5.1.3 on 2024-12-05 08:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_game_file_path_alter_game_discipline"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="teacher",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="students",
                to="core.teacher",
            ),
        ),
    ]
