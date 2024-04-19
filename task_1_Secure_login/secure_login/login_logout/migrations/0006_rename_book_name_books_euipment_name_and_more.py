# Generated by Django 5.0.4 on 2024-04-16 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_logout', '0005_alter_books_requested_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='books',
            old_name='book_name',
            new_name='euipment_name',
        ),
        migrations.AddField(
            model_name='books',
            name='availabilty',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='books',
            name='euipment_type',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
