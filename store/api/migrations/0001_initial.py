# Generated by Django 5.0.6 on 2024-05-25 10:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('creation_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('NEW', 'New'), ('PROCESSED', 'Processed'), ('PAID', 'Paid')], default='NEW', max_length=9)),
                ('creation_date', models.DateField()),
                ('cost', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateField()),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='api.order')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='api.product')),
            ],
        ),
    ]
