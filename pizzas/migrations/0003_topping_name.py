# Generated by Django 3.1.3 on 2020-12-03 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0002_topping'),
    ]

    operations = [
        migrations.AddField(
            model_name='topping',
            name='name',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
