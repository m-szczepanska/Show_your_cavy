# Generated by Django 2.2.6 on 2019-10-16 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creatder', '0003_auto_20191013_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='creature',
            name='crossed_rainbow_bridge',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='creature',
            name='sex',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('NS', 'Not sure')], default='F', max_length=2),
        ),
    ]