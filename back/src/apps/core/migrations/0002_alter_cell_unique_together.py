# Generated by Django 4.1.5 on 2023-01-20 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cell',
            unique_together={('x', 'y')},
        ),
    ]
