from django.urls import path
from . import views

app_name = 'viz'

urlpatterns = [
    path('sna_interactive/', views.sna_interactive, name='sna-interactive'),
    path('wc/', views.wc, name='wc'),
]
