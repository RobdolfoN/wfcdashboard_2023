# Generated by Django 4.0.5 on 2023-12-13 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dddashboard', '0004_companyname_size_alter_companydata_company_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydata',
            name='company_size',
            field=models.CharField(choices=[('small', 'small'), ('medium', 'medium'), ('large', 'large')], max_length=100, null=True),
        ),
    ]
