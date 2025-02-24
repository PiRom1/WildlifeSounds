# Generated by Django 5.1.6 on 2025-02-24 13:32

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genus_name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Taxon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxon_name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Utilisateur',
            },
        ),
        migrations.CreateModel(
            name='Specie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vernacular_name', models.CharField(max_length=100)),
                ('scientific_name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('family', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wildlife_sounds.family')),
                ('genus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wildlife_sounds.genus')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wildlife_sounds.order')),
                ('taxon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wildlife_sounds.taxon')),
            ],
        ),
        migrations.CreateModel(
            name='SpecieSound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sound', models.FileField(upload_to='SpecieSound/')),
                ('type', models.CharField(choices=[('call', 'Call'), ('song', 'Song')], max_length=100)),
                ('country', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('specie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wildlife_sounds.specie')),
            ],
        ),
    ]
