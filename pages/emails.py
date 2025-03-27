from django.core.mail import send_mail
from django.conf import settings

def send_inquiry_email(inquiry):
    subject = "New Inquiry Received"
    message = f"""
    You have received a new inquiry from {inquiry.name}.
    
    Name: {inquiry.name}
    Email: {inquiry.email}
    Phone Number: {inquiry.phone_number}
    
    Message:
    {inquiry.message}
    """

    admin_email = "your_email@yourdomain.com"  # Replace with your Namecheap email
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])


def send_visa_application_email(application):
    subject = "New Visa Application Received"
    message = f"""
    A new visa application has been submitted.

    Applicant Name: {application.applicant_name}
    Email: {application.email}
    Country to Visit: {application.country_to_visit}
    Duration: {application.duration}
    Departure Airport: {application.departure_airport}
    Destination Airport: {application.destination_airport}
    Message: {application.message}

    Submitted on: {application.created_at}
    """

    admin_email = "your_email@yourdomain.com"  # Replace with your Namecheap email
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])
