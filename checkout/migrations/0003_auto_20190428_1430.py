# Generated by Django 2.2 on 2019-04-28 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_auto_20190428_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(db_index=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='email',
            field=models.EmailField(db_index=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='checkout.Order'),
        ),
    ]
