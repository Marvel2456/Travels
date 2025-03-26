from django.urls import path
from . import views


urlpatterns = [
    path('', views.homeView, name='index'),
    path('about/', views.aboutView, name='about'),
    path('contact/', views.contactView, name='contact'),
    path('inquire/', views.inquiryView, name='inquire'),
    path('destination/', views.destinationView, name='destination'),
    path('destination_detail/<uuid:pk>/', views.destinationDetailView, name='destination_detail'),
    path('vacation/', views.vacationView, name='vacation'),
    path('visa-application/', views.applicationView, name='visa_application'),
    path('download-pdf/<uuid:application_id>/', views.download_pdf, name='download_pdf'), 
]
