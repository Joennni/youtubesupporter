# Generated by Django 4.0.5 on 2022-07-22 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_comment1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Capture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mem_name', models.TextField()),
                ('video_name', models.TextField()),
                ('img_path', models.TextField()),
                ('capture_get', models.TextField()),
                ('capture_get_day', models.TextField()),
                ('capture_get_time', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Htag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_no', models.IntegerField()),
                ('h_count', models.IntegerField()),
                ('mem_name', models.TextField()),
                ('video_name', models.TextField()),
                ('h_tag', models.TextField()),
                ('h_tag_get', models.TextField()),
                ('h_tag_get_day', models.TextField()),
                ('h_tag_get_time', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Member_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mem_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Member_time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mem_name', models.TextField()),
                ('activation', models.TextField()),
                ('activation_day', models.TextField()),
                ('activation_time', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_no', models.IntegerField()),
                ('script_count', models.IntegerField()),
                ('mem_name', models.TextField()),
                ('video_name', models.TextField()),
                ('time', models.TextField()),
                ('script', models.TextField()),
                ('script_get', models.TextField()),
                ('script_get_day', models.TextField()),
                ('script_get_time', models.TextField()),
            ],
        ),
    ]
