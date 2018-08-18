from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sna_auto', views.sna_auto, name='sna_auto'),
    path('wc_auto', views.wc_auto, name='wc_auto'),
    path('sna', views.sna, name='sna'),
    path('wc', views.wc, name='wc')
]