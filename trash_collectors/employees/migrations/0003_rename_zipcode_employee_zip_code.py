# Generated by Django 3.2.5 on 2021-10-26 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_alter_employee_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='zipcode',
            new_name='zip_code',
        ),
    ]
