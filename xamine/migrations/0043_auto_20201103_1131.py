# Generated by Django 3.1.2 on 2020-11-03 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xamine', '0042_auto_20201024_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='price',
            field=models.FloatField(default=0.0),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='xamine.order')),
                ('total', models.FloatField(default=0.0)),
                ('Patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xamine.patient')),
            ],
        ),
    ]
