from django.forms import ModelForm
from cms.models import Inquiry, VisaApplication



class InquiryForm(ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone_number', 'message']
        exclude = ['created_at']


class VisaApplicationForm(ModelForm):
    class Meta:
        model = VisaApplication
        fields = ['applicant_name', 'email', 'country_to_visit', 
                  'duration', 'departure_airport', 'destination_airport', 'message']
        exclude = ['created_at']