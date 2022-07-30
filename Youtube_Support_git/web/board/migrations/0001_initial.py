# Generated by Django 4.0.4 on 2022-05-07 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_title', models.CharField(max_length=200)),
                ('question_author', models.CharField(max_length=200)),
                ('question_contents', models.TextField()),
                ('question_date', models.DateTimeField()),
                ('question_view', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_author', models.CharField(max_length=200)),
                ('answer_contents', models.TextField()),
                ('answer_date', models.DateTimeField()),
                ('answer_question_id', models.ForeignKey(db_column='answer_question_id', on_delete=django.db.models.deletion.CASCADE, to='board.question')),
            ],
        ),
    ]
