from django.urls import path
from. import views

urlpatterns = [
    path('', views.home, name='i_home'),
    path('sna_auto', views.sna_auto, name='i_sna_auto'),
    path('wc_auto', views.wc_auto, name='i_wc_auto'),
    path('sna', views.sna, name='i_sna'),
    path('wc', views.wc, name='i_wc')
]