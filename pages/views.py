from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from cms.models import *
from .forms import InquiryForm, VisaApplicationForm
from .emails import send_inquiry_email, send_visa_application_email
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse

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
    inquire_form = InquiryForm()
    if request.method == 'POST':
        inquire_form = InquiryForm(request.POST)
        if inquire_form.is_valid():
            inquiry = inquire_form.save()
            send_inquiry_email(inquiry)
            messages.success(request, 'Your inquiry has been sent successfully')
            inquire_form = InquiryForm()
            return redirect('contact')
    page_detail = PageDetail.objects.all()
    
    context = {
        'page_detail': page_detail,
        'inquire_form': inquire_form
    }
    return render(request, 'pages/contact.html', context)

def inquiryView(request):
    inquire_form = InquiryForm()

    if request.method == 'POST':
        inquire_form = InquiryForm(request.POST)
        if inquire_form.is_valid():
            inquiry = inquire_form.save()

            # Send email notification
            send_inquiry_email(inquiry)

            # Show success message
            messages.success(request, 'Your inquiry has been sent successfully')

            # Redirect to prevent resubmission on page refresh
            return redirect('index')

    context = {'inquire_form': inquire_form}
    return render(request, 'pages/inquire.html', context)

def destinationView(request):
    page_detail = PageDetail.objects.all()
    destination = Destination.objects.all()
    context = {
        'page_detail': page_detail,
        'destination': destination
    }
    return render(request, 'pages/destination.html', context)

def vacationView(request):
    query = request.GET.get('search', '')  # Get search query from URL

    # Filter destinations based on name or location
    if query:
        destination = Destination.objects.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )
    else:
        destination = Destination.objects.all()

    page_detail = PageDetail.objects.all()

    context = {
        'page_detail': page_detail,
        'destination': destination,
        'query': query  # Pass the query back to template
    }
    return render(request, 'pages/vacation.html', context)


def destinationDetailView(request, pk):
    destination = Destination.objects.get(id=pk)
    page_detail = PageDetail.objects.all()
    context = {
        'page_detail': page_detail,
        'destination': destination,
    }
    return render(request, 'pages/destination_detail.html', context)


def applicationView(request):
    form = VisaApplicationForm()

    if request.method == 'POST':
        form = VisaApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()

            # Send email to admin
            send_visa_application_email(application)

            # Redirect to PDF download view with application ID
            return redirect('download_pdf', application_id=application.id)  

    page_detail = PageDetail.objects.all()
    context = {
        'page_detail': page_detail,
        'form': form
    }
    return render(request, 'pages/application.html', context)


def download_pdf(request, application_id):
    try:
        application = VisaApplication.objects.get(id=application_id)
    except VisaApplication.DoesNotExist:
        return HttpResponse("Application not found.", content_type="text/plain")

    # Load template
    template_path = 'pages/visa_pdf.html'
    context = {'application': application}
    template = get_template(template_path)
    html = template.render(context)

    # Generate PDF
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", content_type='text/plain')

    pdf.seek(0)

    # Return PDF response
    response = HttpResponse(pdf.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="visa_application.pdf"'
    return response