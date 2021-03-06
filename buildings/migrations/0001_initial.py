# Generated by Django 2.0.3 on 2018-04-22 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalRoomEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('number_of_animals', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AnimalRoomExit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('number_of_animals', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AnimalRoomTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildings.AnimalRoomEntry')),
                ('room_exit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildings.AnimalRoomExit')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('is_separation', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RoomGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Silo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.FloatField()),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('roomgroup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='buildings.RoomGroup')),
                ('location', models.CharField(blank=True, max_length=150)),
            ],
            bases=('buildings.roomgroup',),
        ),
        migrations.AddField(
            model_name='roomgroup',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='buildings.RoomGroup'),
        ),
        migrations.AddField(
            model_name='room',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildings.RoomGroup'),
        ),
        migrations.AddField(
            model_name='animalroomexit',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildings.Room'),
        ),
        migrations.AddField(
            model_name='animalroomentry',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildings.Room'),
        ),
        migrations.AddField(
            model_name='silo',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildings.Building'),
        ),
    ]
