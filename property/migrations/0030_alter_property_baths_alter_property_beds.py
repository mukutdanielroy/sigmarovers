# Generated by Django 4.2.10 on 2024-02-22 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0029_property_baths_property_beds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='baths',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.bath'),
        ),
        migrations.AlterField(
            model_name='property',
            name='beds',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.bed'),
        ),
    ]
