# Generated by Django 2.2.3 on 2020-02-15 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_name', models.CharField(max_length=100)),
                ('channel_type', models.CharField(choices=[('CTRL', 'control')], max_length=100)),
            ],
        ),
    ]