from django.shortcuts import render
from cms.models import *

# Create your views here.


def homeView(request):
    page_detail = PageDetail.objects.all()
    context = {
        'page_detail': page_detail
    }
    return render(request, 'pages/index.html', context)

def aboutView(request):
    page_detail = PageDetail.objects.all()
    context = {
        'page_detail': page_detail
    }
    return render(request, 'pages/about.html', context)

def contactView(request):
    page_detail = PageDetail.objects.all()
    
    context = {
        'page_detail': page_detail
    }
    return render(request, 'pages/contact.html', context)

def destinationView(request):
    page_detail = PageDetail.objects.all()
    destination = Destination.objects.all()
    context = {
        'page_detail': page_detail,
        'destination': destination
    }
    return render(request, 'pages/destination.html', context)

def vacationView(request):
    page_detail = PageDetail.objects.all()
    destination = Destination.objects.all()
    context = {
        'page_detail': page_detail,
        'destination': destination
    }
    return render(request, 'pages/vacation.html', context)

def destinationDetailView(request, pk):
    destination = Destination.objects.get(uuid=pk)
    page_detail = PageDetail.objects.all()
    context = {
        'page_detail': page_detail,
        'destination': destination,
    }
    return render(request, 'pages/destination_detail.html', context)
