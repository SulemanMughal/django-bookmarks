# Generated by Django 3.1.4 on 2021-07-07 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0004_sharedbookmark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharedbookmark',
            name='bookmark',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmarks.bookmark'),
        ),
    ]
