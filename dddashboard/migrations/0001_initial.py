# Generated by Django 4.0.5 on 2024-02-12 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dashboard_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('company_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dddashboard.companyname')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'verbose_name_plural': 'Dashboard Users',
            },
        ),
        migrations.CreateModel(
            name='CompanyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_size', models.CharField(choices=[('small', 'small'), ('medium', 'medium'), ('large', 'large')], max_length=100, null=True)),
                ('gender_code', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=6, null=True)),
                ('aboriginal_peoples', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=3, null=True)),
                ('visible_minorities', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=3, null=True)),
                ('person_with_disabilities', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=3, null=True)),
                ('position_category', models.CharField(choices=[('Executive', 'Executive'), ('Senior Leader', 'Senior Leader'), ('Manager/Supervisor/Superintendent', 'Manager/Supervisor/Superintendent'), ('Foreperson', 'Foreperson'), ('Individual Contributor', 'Individual Contributor')], max_length=500, null=True)),
                ('year_created', models.DateField()),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_data_names', to='dddashboard.companyname')),
            ],
            options={
                'verbose_name': 'Company Data',
                'verbose_name_plural': 'Company Data',
            },
        ),
    ]
