# Generated by Django 3.1.6 on 2021-02-20 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='shortBio',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='biography',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='description',
            field=models.TextField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='fullName',
            field=models.CharField(max_length=20),
        ),
    ]
