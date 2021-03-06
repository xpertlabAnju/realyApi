# Generated by Django 3.2.12 on 2022-03-20 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='chatDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatId', models.IntegerField()),
                ('senderId', models.IntegerField()),
                ('receiverId', models.IntegerField()),
                ('senderType', models.CharField(blank=True, max_length=255, null=True)),
                ('receiverType', models.CharField(blank=True, max_length=255, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('delete', models.SmallIntegerField(default='0')),
            ],
        ),
    ]
