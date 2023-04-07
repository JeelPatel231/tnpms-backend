from django.contrib import admin
from company import models as m
from django.contrib.admin import ModelAdmin
from tnpapp import settings
from user.models import Student
from django.core.mail import send_mass_mail

# Register your models here.


@admin.register(m.Company)
class CompanyAdmin(ModelAdmin):
    list_display = (
        "name",
        "email_id",
        "hr_name",
        "industry_type",
        "company_type",
    )

class OpeningForDepartmentInline(admin.TabularInline):
    model = m.OpeningForDepartment

@admin.register(m.CurrentOpening)
class CurrentOpeningsAdmin(ModelAdmin):
    # TODO : generate message body and send emails to filtered out students
    @admin.action(description="Notify students")
    def notify_students_opening(self, request, queryset):
        interested_students = Student.objects.filter(is_blocked=False)
        # also filter through their departments
        student_emails = [s.email for s in interested_students]
        # make multiple message bodies from queryset and use send_mass_mail
        all_emails = []
        for i in queryset:
            print(i)
            # construct message body using title and description of the opening
            # all_emails.append(message_body)
        # send_mass_mail(all_emails, fail_silently=False)

    actions = ("notify_students_opening",)
    inlines = (OpeningForDepartmentInline,)
    list_display = (
        "job_title",
        "company",
        "opening_year",
        "nature_of_job",
        "vacancy_count",
        "min_package",
        "gender_preference",
    )
