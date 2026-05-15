from django.db import migrations
import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', django.db.models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', django.db.models.CharField(max_length=128, verbose_name='password')),
                ('last_login', django.db.models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', django.db.models.BooleanField(default=False)),
                ('username', django.db.models.CharField(max_length=150, unique=True)),
                ('first_name', django.db.models.CharField(blank=True, max_length=150)),
                ('last_name', django.db.models.CharField(blank=True, max_length=150)),
                ('email', django.db.models.EmailField(blank=True, max_length=254)),
                ('is_staff', django.db.models.BooleanField(default=False)),
                ('is_active', django.db.models.BooleanField(default=True)),
                ('date_joined', django.db.models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', django.db.models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='auth.group')),
                ('user_permissions', django.db.models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]