from django.urls import path
from . import views

app_name = 'viz'

urlpatterns = [
    path('sna_interactive/', views.sna_interactive, name='sna-interactive'),
    path('sna_interactive_file/', views.sna_interactive_file, name='sna-interactive-file'),
    path('wc/', views.wc, name='wc'),
    path('wc_file/', views.wc_file, name='wc-file'),
]
