# Generated by Django 5.1 on 2024-08-25 04:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=100)),
                ('book_image', models.CharField(blank=True, default='', max_length=256)),
                ('author', models.CharField(max_length=50)),
                ('publisher', models.CharField(max_length=50)),
                ('keywords', models.JSONField(default=list)),
                ('entire_pages', models.IntegerField()),
            ],
            options={
                'db_table': 'Book',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BookSentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=100)),
                ('represent_sentence', models.JSONField(default=list)),
            ],
            options={
                'db_table': 'BookSentence',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=1)),
                ('reading_time', models.JSONField(default=dict)),
                ('reading_pages', models.IntegerField(default=0)),
                ('reading_days', models.JSONField(default=list)),
                ('saved_at', models.DateField()),
            ],
            options={
                'db_table': 'UserBook',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BookDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro', models.TextField()),
                ('buying_at', models.JSONField(default=dict)),
                ('book', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='book.book')),
            ],
            options={
                'db_table': 'BookDetail',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BriefReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brief_review', models.TextField()),
                ('written_at', models.DateField()),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book.book')),
            ],
            options={
                'db_table': 'BriefReview',
                'managed': True,
            },
        ),
    ]
