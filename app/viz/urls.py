from django.urls import path
from . import views

app_name = 'viz'

urlpatterns = [
    path('sna_interactive/', views.sna_interactive, name='sna_interactive'),
    path('sna_interactive_file/', views.sna_interactive_file, name='sna_interactive_file'),
    path('sna_gexf/', views.get_gexf, name='get_gexf'),
    path('sna/', views.sna, name='sna'),
    path('sna_file/', views.sna_file, name='sna_file'),
    path('sna_result/', views.sna_result, name='sna_result'),
    path('wc/', views.wc, name='wc'),
    path('wc_file/', views.wc_file, name='wc_file'),
    path('wc_result/', views.wc_result, name='wc_result'),
]