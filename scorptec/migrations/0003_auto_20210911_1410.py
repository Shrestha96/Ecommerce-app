# Generated by Django 3.2.5 on 2021-09-11 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorptec', '0002_categories'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='categories_name',
            new_name='category_name',
        ),
    ]
