# Generated by Django 3.0.6 on 2020-06-08 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_delete_refund'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='stripe_charge_id',
        ),
    ]