import os
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
from django.conf import settings
from django.templatetags.static import static
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from datetime import datetime

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

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="visa_application.pdf"'

    pdf = canvas.Canvas(response)

    # ✅ Load logo
    logo_path = os.path.join(settings.BASE_DIR, 'travel/static/assets/img/assurance_logo.png')
    
    if not os.path.exists(logo_path):
        return HttpResponse("Logo not found at: " + logo_path, content_type="text/plain")

    # ✅ Set margin/padding
    left_margin = 60
    top_margin = 780
    line_spacing = 20  # Spacing between lines

    # ✅ Draw the logo on the left
    logo_width = 60
    logo_height = 50
    pdf.drawImage(ImageReader(logo_path), left_margin, top_margin, width=logo_width, height=logo_height)

    # ✅ Add company name beside the logo
    pdf.setFont("Helvetica-Bold", 16)
    company_name = "Assurance International Travels"
    pdf.drawString(left_margin + logo_width + 20, top_margin + 15, company_name)

    # ✅ Draw underline for the company name
    text_width = pdf.stringWidth(company_name, "Helvetica-Bold", 16)
    pdf.line(left_margin + logo_width + 20, top_margin + 13, left_margin + logo_width + 20 + text_width, top_margin + 13)

    # ✅ Move to content area
    start_y = top_margin - 60  

    # ✅ Convert submitted date to only show YYYY-MM-DD
    submitted_date = application.created_at.strftime("%Y-%m-%d")

    # ✅ Set font and draw application details with proper spacing
    pdf.setFont("Helvetica", 12)
    pdf.drawString(left_margin, start_y, f"Applicant Name: {application.applicant_name}")
    pdf.drawString(left_margin, start_y - line_spacing, f"Email: {application.email}")
    pdf.drawString(left_margin, start_y - (2 * line_spacing), f"Country to Visit: {application.country_to_visit}")
    pdf.drawString(left_margin, start_y - (3 * line_spacing), f"Duration: {application.duration} months")
    pdf.drawString(left_margin, start_y - (4 * line_spacing), f"Departure Airport: {application.departure_airport}")
    pdf.drawString(left_margin, start_y - (5 * line_spacing), f"Destination Airport: {application.destination_airport}")
    pdf.drawString(left_margin, start_y - (6 * line_spacing), f"Message: {application.message}")
    pdf.drawString(left_margin, start_y - (7 * line_spacing), f"Submitted On: {submitted_date}")

    pdf.showPage()
    pdf.save()

    return response