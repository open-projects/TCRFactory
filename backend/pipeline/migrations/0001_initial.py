# Generated by Django 3.1.2 on 2021-02-18 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_id', models.IntegerField(db_index=True)),
                ('thread', models.IntegerField(db_index=True, default=0, unique=True)),
                ('pid', models.IntegerField(db_index=True, default=0)),
                ('cmd', models.CharField(max_length=200)),
                ('output_file', models.CharField(default='', max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]