# Generated by Django 2.1.2 on 2018-10-20 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eprint_users', '0005_printdocs_num_pages'),
    ]

    operations = [
        migrations.AddField(
            model_name='printdocs',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='printdocs',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
