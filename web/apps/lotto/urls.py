from django.urls import path
from . import views

app_name = 'lotto'

urlpatterns = [
    # 일반 사용자
    path('', views.LottoHomeView.as_view(), name='home'),
    path('buy/', views.BuyTicketView.as_view(), name='buy'),
    path('my-tickets/', views.MyTicketsView.as_view(), name='my_tickets'),
    path('check/<int:ticket_id>/', views.CheckPrizeView.as_view(), name='check'),

    # 관리자
    path('admin-lotto/dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin-lotto/sales/', views.AdminSalesView.as_view(), name='admin_sales'),
    path('admin-lotto/draw/<int:round_no>/', views.AdminDrawView.as_view(), name='admin_draw'),
    path('admin-lotto/results/', views.AdminResultsView.as_view(), name='admin_results'),
]