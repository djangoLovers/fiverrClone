# Generated by Django 3.1.6 on 2021-02-21 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0003_gig_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='gig',
            name='description',
            field=models.CharField(max_length=90, null=True),
        ),
    ]
