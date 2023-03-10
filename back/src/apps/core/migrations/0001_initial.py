# Generated by Django 4.1.5 on 2023-01-20 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField(verbose_name='X координата')),
                ('y', models.IntegerField(verbose_name='Y координата')),
            ],
        ),
        migrations.CreateModel(
            name='World',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WorldCell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alive', models.BooleanField(default=False)),
                ('cell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='world_cells', related_query_name='world_cells', to='core.cell')),
                ('world', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='world_cells', related_query_name='world_cells', to='core.world')),
            ],
        ),
        migrations.AddField(
            model_name='world',
            name='cells',
            field=models.ManyToManyField(related_name='worlds', related_query_name='worlds', through='core.WorldCell', to='core.cell'),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generation_num', models.IntegerField(verbose_name='Номер генерации')),
                ('state_hash', models.CharField(max_length=64, verbose_name='Хэш состояния')),
                ('world', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='states', related_query_name='states', to='core.world')),
            ],
        ),
        migrations.AddIndex(
            model_name='cell',
            index=models.Index(fields=['x', 'y'], name='core_cell_x_c4d660_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='worldcell',
            unique_together={('cell', 'world')},
        ),
    ]
