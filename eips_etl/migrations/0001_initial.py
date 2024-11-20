# Generated by Django 5.1.2 on 2024-11-20 01:25

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('person_id', models.AutoField(primary_key=True, serialize=False)),
                ('person_string', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('commit_id', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('author_time', models.DateTimeField()),
                ('commit_time', models.DateTimeField()),
                ('gpg_sig', models.TextField(default='')),
                ('message', models.TextField(default='')),
                ('parents', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=40), size=None)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='eips_etl.person')),
                ('committer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='committer', to='eips_etl.person')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('document_id', models.IntegerField()),
                ('document_type', models.CharField(choices=[('EIP', 'EIP'), ('ERC', 'ERC')], max_length=3)),
                ('created', models.DateTimeField(null=True)),
                ('updated', models.DateTimeField(default=None, null=True)),
                ('status', models.CharField(choices=[('LIVING', 'Living'), ('IDEA', 'Idea'), ('DRAFT', 'Draft'), ('REVIEW', 'Review'), ('LAST_CALL', 'Last Call'), ('FINAL', 'Final'), ('STAGNANT', 'Stagnant'), ('WITHDRAWN', 'Withdrawn'), ('ABANDONED', 'Abandoned'), ('ACCEPTED', 'Accepted'), ('ACTIVE', 'Active'), ('DEFERRED', 'Deferred'), ('REJECTED', 'Rejected'), ('REPLACED', 'Replaced'), ('SUPERSEDED', 'Superseded'), ('MOVED', 'Moved'), ('ERROR', 'Error')], max_length=20)),
                ('category', models.CharField(blank=True, choices=[('CORE', 'Core'), ('NETWORKING', 'Networking'), ('INTERFACE', 'Interface'), ('ERC', 'ERC')], default='', max_length=20)),
                ('type', models.CharField(blank=True, choices=[('STANDARDS', 'Standards Track'), ('INFORMATIONAL', 'Informational'), ('META', 'Meta')], default='', max_length=20)),
                ('resolution', models.CharField(blank=True, default='', max_length=1024)),
                ('title', models.CharField(blank=True, default='', max_length=1024)),
                ('discussions_to', models.CharField(blank=True, default='', max_length=2048)),
                ('review_period_end', models.CharField(blank=True, default='', max_length=2048)),
                ('requires', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('replaces', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('superseded_by', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('description', models.TextField()),
                ('body', models.TextField()),
                ('error_message', models.CharField(blank=True, default='', max_length=2028)),
                ('commit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eips_etl.commit')),
                ('authors', models.ManyToManyField(to='eips_etl.person')),
            ],
            options={
                'indexes': [models.Index(fields=['document_id', 'document_type'], name='eips_etl_do_documen_f94a07_idx'), models.Index(fields=['commit'], name='eips_etl_do_commit__c1c242_idx')],
                'unique_together': {('document_id', 'commit')},
            },
        ),
    ]
