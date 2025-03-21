from django.db import models
import uuid

# Create your models here.


class Destination(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    thumbnail = models.ImageField(upload_to='pics', blank=True, null=True)
    image_1 = models.ImageField(upload_to='pics', blank=True, null=True)
    image_2 = models.ImageField(upload_to='pics', blank=True, null=True)
    image_3 = models.ImageField(upload_to='pics', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name
    

class PageDetail(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=250, blank=True, null=True)
    email_1 = models.CharField(max_length=250, blank=True, null=True)
    email_2 = models.CharField(max_length=250, blank=True, null=True)
    

    def __str__(self):
        return self.phone_number
    

class Inquiry(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    phone_number = models.CharField(max_length=250, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name
    

class VisaApplication(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    applicant_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    country_to_visit = models.CharField(max_length=250, blank=True, null=True)
    duratrion_choice = {
        ('3 months', '3 months'),
        ('6 months', '6 months'),
        ('12 months', '12 months'),
       
    }
    duration = models.CharField(max_length=250, choices=duratrion_choice, blank=True, null=True)
    departure_airpot = models.CharField(max_length=250, blank=True, null=True)
    destination_airport = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.applicant_name