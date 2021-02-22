# Generated by Django 3.1.6 on 2021-02-22 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0004_gig_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gig',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, related_name='gigs_category', to='gigs.Category'),
        ),
    ]
