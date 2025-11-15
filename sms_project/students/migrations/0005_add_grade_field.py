# Generated migration file

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_add_subject_to_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='grade',
            field=models.CharField(blank=True, choices=[('A', 'A (90-100)'), ('B', 'B (80-89)'), ('C', 'C (70-79)'), ('D', 'D (60-69)'), ('F', 'F (Below 60)')], max_length=1, null=True),
        ),
    ]
