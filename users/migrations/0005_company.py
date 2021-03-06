# Generated by Django 2.2.1 on 2020-10-04 14:33

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190811_1824'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('status', django_enumfield.db.fields.EnumField(default=0, enum=users.models.CompanyStatus)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('coordinates', django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=6, max_digits=9), blank=True, null=True, size=2)),
                ('site', models.URLField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
