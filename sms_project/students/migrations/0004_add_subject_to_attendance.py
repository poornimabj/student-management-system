# Migration: add subject field to Attendance
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_activitylog'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='subject',
            field=models.CharField(default='General', max_length=120),
            preserve_default=False,
        ),
    ]
