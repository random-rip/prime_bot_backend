# Generated by Django 3.0.8 on 2020-07-04 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_prime_league', '0005_player_summoner_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='latest_suggestion',
            field=models.TextField(null=True),
        ),
        migrations.DeleteModel(
            name='Log',
        ),
    ]
