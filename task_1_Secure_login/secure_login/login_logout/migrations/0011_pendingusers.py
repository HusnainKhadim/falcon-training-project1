# Generated by Django 5.0.4 on 2024-04-17 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_logout', '0010_bookedequipments_delete_issuedbooks'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=150)),
            ],
        ),
    ]
