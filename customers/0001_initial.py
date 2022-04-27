# Generated by Django 3.2.12 on 2022-02-26 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomersCustomers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(blank=True, max_length=50, null=True)),
                ('firstname', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(max_length=50)),
                ('number', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.CharField(max_length=100)),
                ('otp', models.IntegerField()),
                ('profilepic', models.CharField(blank=True, max_length=100, null=True)),
                ('allownotification', models.SmallIntegerField(db_column='allowNotification')),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('delete', models.SmallIntegerField()),
                ('type', models.SmallIntegerField()),
                ('status', models.SmallIntegerField(blank=True, null=True)),
                ('isrequested', models.SmallIntegerField(db_column='isRequested')),
                ('document', models.CharField(blank=True, max_length=200, null=True)),
                ('rejectionreason', models.TextField(blank=True, db_column='rejectionReason', null=True)),
                ('dob', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
