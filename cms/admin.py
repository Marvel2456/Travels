from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin

# Register your models here.

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

@admin.register(Destination)
class DestinationAdmin(ModelAdmin):
    list_display = ['name', 'location']
    search_fields = ['name', 'location']
    list_filter = ['location']

@admin.register(Inquiry)
class InquiryAdmin(ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']


@admin.register(PageDetail)
class PageDetailAdmin(ModelAdmin):
    list_display = ['phone_number', 'email_1', 'email_2']
    search_fields = ['phone_number', 'email_1', 'email_2']
    list_filter = ['phone_number', 'email_1', 'email_2']


@admin.register(VisaApplication)
class VisaApplicationAdmin(ModelAdmin):
    list_display = ['applicant_name', 'email', 'duration', 'country_to_visit', 'created_at']
    search_fields = ['applicant_name', 'email', 'country_to_visit']
    list_filter = ['country_to_visit', 'created_at']

