from django.urls import path
from . import views


urlpatterns = [
    path('', views.homeView, name='index'),
    path('about/', views.aboutView, name='about'),
    path('contact/', views.contactView, name='contact'),
    path('destination/', views.destinationView, name='destination'),
    path('destination_detail/<uuid:str>/', views.destinationDetailView, name='destination_detail'),
    path('vacation/', views.vacationView, name='vacation'),
]
