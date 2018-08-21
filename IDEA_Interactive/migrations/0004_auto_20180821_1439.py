# Generated by Django 2.0.3 on 2018-08-21 05:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IDEA_Interactive', '0003_auto_20180821_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelautosna',
            name='node_num',
            field=models.IntegerField(default=30, validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='modelsna',
            name='edge_remove_threshold',
            field=models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
        ),
        migrations.AlterField(
            model_name='modelsna',
            name='node_num',
            field=models.IntegerField(default=30, validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
