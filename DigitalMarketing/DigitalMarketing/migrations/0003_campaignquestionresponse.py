# Generated by Django 4.1.7 on 2023-08-12 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DigitalMarketing', '0002_delete_campaignquestionresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaignquestionresponse',
            fields=[
                ('response', models.CharField(db_column='response', max_length=2000, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'campaignquestionresponse',
                'managed': False,
            },
        ),
    ]
