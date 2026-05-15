from django.db import migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Draw',
            fields=[
                ('id', django.db.models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_no', django.db.models.PositiveIntegerField(unique=True, verbose_name='회차')),
                ('draw_date', django.db.models.DateField(verbose_name='추첨일')),
                ('numbers', django.db.models.JSONField(blank=True, null=True)),
                ('bonus', django.db.models.IntegerField(blank=True, null=True)),
                ('status', django.db.models.CharField(choices=[('pending', '대기'), ('drawn', '추첨완료')], default='pending', max_length=10)),
            ],
            options={
                'ordering': ['-round_no'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', django.db.models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numbers', django.db.models.JSONField()),
                ('purchase_type', django.db.models.CharField(choices=[('manual', '수동'), ('auto', '자동')], max_length=6)),
                ('prize_rank', django.db.models.IntegerField(choices=[(0, '낙첨'), (1, '1등'), (2, '2등'), (3, '3등'), (4, '4등'), (5, '5등')], default=0)),
                ('prize_amount', django.db.models.BigIntegerField(default=0)),
                ('created_at', django.db.models.DateTimeField(auto_now_add=True)),
                ('draw', django.db.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='lotto.draw')),
                ('user', django.db.models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]