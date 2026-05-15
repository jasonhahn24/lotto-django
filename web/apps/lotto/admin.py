from django.contrib import admin
from .models import Draw, Ticket

@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = ['round_no', 'draw_date', 'status', 'numbers', 'bonus']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'draw', 'numbers', 'purchase_type', 'prize_rank']