from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('IDEA_Interactive/', include('IDEA_Interactive.urls')),
    path('IDEA_Interactive/', views.interactive, name='IDEA_Interactive'),
    path('IDEA_Simple/', include('IDEA_Simple.urls')),
    path('IDEA_Simple/', views.simple, name='IDEA_Simple'),
]