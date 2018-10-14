# Generated by Django 2.0.3 on 2018-10-04 15:37

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import storageApp.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InputSignal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('adnotations', models.TextField(blank=True, null=True)),
                ('amplitude_unit', models.CharField(max_length=64)),
                ('sample_rate', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-10)])),
                ('input_file', models.FileField(upload_to='signals/', validators=[storageApp.validators.validate_input_file_extension])),
                ('results_file', models.FileField(blank=True, default='results/results_template.json', null=True, upload_to='results/', validators=[storageApp.validators.validate_results_file_extension])),
                ('add_date', models.DateTimeField(default=datetime.datetime(2018, 10, 4, 17, 37, 32, 999568))),
                ('last_edit_date', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]