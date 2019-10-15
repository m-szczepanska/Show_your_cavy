# Generated by Django 2.2.6 on 2019-10-13 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creatder', '0002_auto_20191010_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creature',
            name='breed',
            field=models.CharField(choices=[('OT', 'Other'), ('AM', 'American'), ('AB', 'Abyssinian'), ('HR', 'Hairless'), ('HI', 'Himalayan'), ('PR', 'Peruvian'), ('RX', 'Rex'), ('SL', 'Silkie'), ('TD', 'Teddy'), ('WD', 'White-crested')], default='OT', max_length=2),
        ),
        migrations.AlterField(
            model_name='creature',
            name='color_pattern',
            field=models.CharField(choices=[('BL', 'Self-Black'), ('WH', 'Self-White'), ('RD', 'Self-Red'), ('CR', 'Self-Cream'), ('CH', 'Agouti-Chocolate'), ('AG', 'Agouti-Golde'), ('AV', 'Agouti-Silver'), ('AC', 'Agouti-Cream'), ('WB', 'White-black'), ('WR', 'White-red'), ('SB', 'Red-black'), ('WC', 'White-cream'), ('BR', 'Brindle'), ('MX', 'Mix'), ('AL', 'Albino')], default='MX', max_length=2),
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
