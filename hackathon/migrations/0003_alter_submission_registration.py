# Generated by Django 4.2 on 2023-04-17 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("hackathon", "0002_alter_submission_file_alter_submission_registration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="submission",
            name="registration",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="hackathon.registration"
            ),
        ),
    ]
