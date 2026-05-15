from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import FormView, ListView, DetailView, TemplateView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Sum
from django.http import HttpResponseForbidden

from .models import Draw, Ticket
from .forms import TicketPurchaseForm
from .utils import generate_auto_numbers, check_prize_rank


class LottoHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'lotto/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['latest_draw'] = Draw.objects.filter(status='drawn').first()
        ctx['pending_draw'] = Draw.objects.filter(status='pending').first()
        return ctx


class BuyTicketView(LoginRequiredMixin, FormView):
    template_name = 'lotto/buy.html'
    form_class = TicketPurchaseForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pending_draw'] = Draw.objects.filter(status='pending').first()
        return ctx

    def form_valid(self, form):
        draw = Draw.objects.filter(status='pending').first()
        if not draw:
            messages.error(self.request, '현재 구매 가능한 회차가 없습니다.')
            return redirect('lotto:buy')

        ptype = form.cleaned_data['purchase_type']
        if ptype == 'auto':
            nums = generate_auto_numbers()
        else:
            nums = sorted([
                form.cleaned_data[f'num{i}'] for i in range(1, 7)
            ])

        with transaction.atomic():
            Ticket.objects.create(
                user=self.request.user,
                draw=draw,
                numbers=nums,
                purchase_type=ptype,
            )

        messages.success(self.request, f'🎰 구매 완료! 선택 번호: {nums}')
        return redirect('lotto:my_tickets')


class MyTicketsView(LoginRequiredMixin, ListView):
    template_name = 'lotto/my_tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(
            user=self.request.user
        ).select_related('draw').order_by('-created_at')


class CheckPrizeView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'lotto/check.html'
    pk_url_kwarg = 'ticket_id'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            return None
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return HttpResponseForbidden('본인 티켓만 확인할 수 있습니다.')
        ctx = self.get_context_data(object=self.object)
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        draw = self.object.draw
        if draw.status == 'drawn':
            rank, desc = check_prize_rank(
                self.object.numbers, draw.numbers, draw.bonus
            )
            ctx['rank'] = rank
            ctx['desc'] = desc
        return ctx


class AdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class AdminDashboardView(AdminMixin, TemplateView):
    template_name = 'lotto/admin/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_tickets'] = Ticket.objects.count()
        ctx['total_revenue'] = Ticket.objects.count() * 1000
        ctx['draws'] = Draw.objects.all()[:10]
        ctx['prize_stats'] = (
            Ticket.objects.exclude(prize_rank=0)
            .values('prize_rank')
            .annotate(cnt=Count('id'), total=Sum('prize_amount'))
            .order_by('prize_rank')
        )
        return ctx


class AdminSalesView(AdminMixin, ListView):
    template_name = 'lotto/admin/sales.html'
    context_object_name = 'tickets'
    paginate_by = 20

    def get_queryset(self):
        return Ticket.objects.select_related(
            'user', 'draw'
        ).order_by('-created_at')


class AdminDrawView(AdminMixin, View):
    def post(self, request, round_no):
        draw = get_object_or_404(Draw, round_no=round_no, status='pending')

        winning = generate_auto_numbers()
        bonus = generate_auto_numbers()[0]
        while bonus in winning:
            bonus = generate_auto_numbers()[0]

        draw.numbers = winning
        draw.bonus = bonus
        draw.status = 'drawn'
        draw.save()

        tickets = list(Ticket.objects.filter(draw=draw))
        for ticket in tickets:
            rank, _ = check_prize_rank(ticket.numbers, winning, bonus)
            ticket.prize_rank = rank
            if rank == 5:
                ticket.prize_amount = 5000
            elif rank == 4:
                ticket.prize_amount = 50000
        Ticket.objects.bulk_update(tickets, ['prize_rank', 'prize_amount'])

        messages.success(request, f'{round_no}회 추첨 완료! 당첨번호: {winning}, 보너스: {bonus}')
        return redirect('lotto:admin_dashboard')


class AdminResultsView(AdminMixin, ListView):
    template_name = 'lotto/admin/results.html'
    context_object_name = 'draws'

    def get_queryset(self):
        return Draw.objects.filter(status='drawn')