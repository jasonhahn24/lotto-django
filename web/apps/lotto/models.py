from django.db import models
from django.conf import settings

class Draw(models.Model):
    STATUS = [('pending', '대기'), ('drawn', '추첨완료')]

    round_no   = models.PositiveIntegerField(unique=True, verbose_name='회차')
    draw_date  = models.DateField(verbose_name='추첨일')
    numbers    = models.JSONField(null=True, blank=True)
    bonus      = models.IntegerField(null=True, blank=True)
    status     = models.CharField(max_length=10, choices=STATUS, default='pending')

    class Meta:
        ordering = ['-round_no']

    def __str__(self):
        return f'{self.round_no}회 ({self.get_status_display()})'


class Ticket(models.Model):
    PURCHASE_TYPES = [('manual', '수동'), ('auto', '자동')]
    RANK_CHOICES   = [(0,'낙첨'),(1,'1등'),(2,'2등'),(3,'3등'),(4,'4등'),(5,'5등')]

    user          = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='tickets')
    draw          = models.ForeignKey(Draw, on_delete=models.CASCADE,
                                      related_name='tickets')
    numbers       = models.JSONField()
    purchase_type = models.CharField(max_length=6, choices=PURCHASE_TYPES)
    prize_rank    = models.IntegerField(choices=RANK_CHOICES, default=0)
    prize_amount  = models.BigIntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.draw.round_no}회] {self.user.username} - {self.numbers}'