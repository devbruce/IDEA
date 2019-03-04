from django.urls import path
from . import views

app_name = 'viz'

urlpatterns = [
    path('sna/', views.sna, name='sna'),
    path('get-sna-gexf/', views.get_sna_gexf, name='get-sna-gexf'),
    path('wc/', views.wc, name='wc'),
    path('get-wc-png/', views.get_wc_png, name='get-wc-png'),
]
