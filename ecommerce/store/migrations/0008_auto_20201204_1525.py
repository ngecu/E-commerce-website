# Generated by Django 3.1.3 on 2020-12-04 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20201204_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saveditems',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.customer'),
        ),
    ]