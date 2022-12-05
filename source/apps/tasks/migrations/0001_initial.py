# Generated by Django 3.2.12 on 2022-12-05 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('assignees', models.ManyToManyField(blank=True, related_name='tasks', to='projects.Member', verbose_name='Assignees')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.project', verbose_name='Project')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
        ),
    ]