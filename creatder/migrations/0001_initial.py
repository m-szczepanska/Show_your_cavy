# Generated by Django 2.2.6 on 2019-10-07 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Creature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('breed', models.CharField(choices=[('OT', 'Other'), ('AM', 'American'), ('AB', 'Abyssinian'), ('HR', 'Hairless'), ('HI', 'Himalayan'), ('PR', 'Peruvian'), ('RX', 'Rex'), ('SL', 'Silkie'), ('TD', 'Teddy'), ('WD', 'White-crested')], default='OT', max_length=255)),
                ('color_pattern', models.CharField(choices=[('BL', 'Self-Black'), ('WH', 'Self-White'), ('RD', 'Self-Red'), ('CR', 'Self-Cream'), ('CH', 'Agouti-Chocolate'), ('AG', 'Agouti-Golde'), ('AV', 'Agouti-Silver'), ('AC', 'Agouti-Cream'), ('WB', 'White-black'), ('WR', 'White-red'), ('SB', 'Red-black'), ('WC', 'White-cream'), ('BR', 'Brindle'), ('MX', 'Mix'), ('AL', 'Albino')], default='MX', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('login', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('_password', models.CharField(max_length=255)),
                ('about_myself', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('comment', models.CharField(max_length=200)),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('creature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='creatder.Creature')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='creatder.User')),
            ],
        ),
        migrations.AddField(
            model_name='creature',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='creatder.User'),
        ),
    ]