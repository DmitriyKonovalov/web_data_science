# Generated by Django 2.0.5 on 2018-06-04 06:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Имя анализа')),
                ('ws', models.CharField(max_length=20, verbose_name='Сигнал скорости ветра')),
                ('wd', models.CharField(max_length=20, verbose_name='Сигнал направления ветра')),
                ('wd_step', models.FloatField(default=0, verbose_name='Шаг группировки направления')),
                ('wd_start', models.FloatField(default=0, verbose_name='Начало сектора направления')),
                ('wd_stop', models.FloatField(default=0, verbose_name='Конец сектора направления')),
                ('ws_start', models.FloatField(default=0, verbose_name='Начало диапазона скорости')),
                ('ws_stop', models.FloatField(default=0, verbose_name='Конец диапазона скорости')),
                ('date_create', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('file_data', models.FileField(default='', upload_to='upload_data')),
                ('file_zip', models.FileField(default='', upload_to='downloads')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Анализ',
                'verbose_name_plural': 'Анализы',
                'ordering': ['-date_modified'],
            },
        ),
    ]
