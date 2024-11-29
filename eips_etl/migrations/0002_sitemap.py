# Generated by Django 5.1.2 on 2024-11-29 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eips_etl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sitemap',
            fields=[
                ('sitemap_id', models.AutoField(primary_key=True, serialize=False)),
                ('generation_time', models.DateTimeField(auto_now_add=True)),
                ('xml_data', models.TextField()),
            ],
        ),
    ]