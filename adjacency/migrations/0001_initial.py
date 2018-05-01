# Generated by Django 2.0.4 on 2018-05-01 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(verbose_name='Json dump')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
            ],
            options={
                'db_table': 'category_id',
            },
        ),
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=56, unique=True, verbose_name='Category name')),
                ('local_id', models.PositiveIntegerField(db_index=True, default=1, verbose_name='Local Graph id')),
                ('father', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Father')),
                ('path', models.TextField(verbose_name='Path to node')),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='adjacency.CategoryId', verbose_name='Category id')),
            ],
            options={
                'db_table': 'category',
            },
        ),
    ]
