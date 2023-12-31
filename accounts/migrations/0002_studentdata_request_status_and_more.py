# Generated by Django 4.1.7 on 2023-10-23 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentdata',
            name='request_status',
            field=models.CharField(default='No Request', max_length=100),
        ),
        migrations.AddField(
            model_name='studentdata',
            name='requested_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
