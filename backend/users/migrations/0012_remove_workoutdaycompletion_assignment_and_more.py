from django.db import migrations, models

def noop(apps, schema_editor):
    return

class Migration(migrations.Migration):

    dependencies = [
        ("users", "0011_delete_fitnessgoal"),
    ]

    operations = [
        # Keep the new profile fields
        migrations.AddField(
            model_name="userprofile",
            name="current_streak",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="last_streak_date",
            field=models.DateField(blank=True, null=True),
        ),
        # Use a noop RunPython so the migration can be applied safely.
        migrations.RunPython(noop, reverse_code=migrations.RunPython.noop),
    ]
