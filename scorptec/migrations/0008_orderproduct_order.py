# Generated by Django 3.2.5 on 2021-09-23 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scorptec', '0007_order_orderproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scorptec.order'),
        ),
    ]
