# Generated by Django 5.0.6 on 2024-07-06 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authDbs', '0001_initial'),
        ('organisation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='organisation',
            field=models.ManyToManyField(blank=True, to='organisation.organisation'),
        ),
    ]
