# Generated by Django 3.1.2 on 2021-02-18 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_id', models.IntegerField(db_index=True)),
                ('name', models.CharField(default='', max_length=200)),
                ('project', models.CharField(max_length=200)),
                ('ident', models.CharField(max_length=200)),
                ('plate', models.CharField(default='', max_length=200)),
                ('well', models.CharField(default='', max_length=200)),
                ('cell_number', models.IntegerField(default=0)),
                ('read_number', models.IntegerField(default=0)),
                ('smart_name', models.CharField(default='', max_length=200)),
                ('smart_benchling', models.CharField(default='', max_length=200)),
                ('alfa_subsample_ident', models.CharField(default='', max_length=200)),
                ('alfa_index_name', models.CharField(default='', max_length=200)),
                ('alfa_index_benchling', models.CharField(default='', max_length=200)),
                ('beta_subsample_ident', models.CharField(default='', max_length=200)),
                ('beta_index_name', models.CharField(default='', max_length=200)),
                ('beta_index_benchling', models.CharField(default='', max_length=200)),
                ('comments', models.TextField(default='')),
                ('date', models.DateField(auto_now_add=True)),
                ('owner', models.CharField(default='Unknown', max_length=200)),
            ],
        ),
    ]