from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('lotto/', include('apps.lotto.urls', namespace='lotto')),
    path('', lambda request: redirect('lotto:home')),
]