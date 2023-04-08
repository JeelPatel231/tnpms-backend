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
        all_emails = []
        for opening in queryset:
            # get all departments, that this opening is avaialable for
            opening_departments = [
                i.dept_id
                for i in m.OpeningForDepartment.objects.filter(opening_id=opening.id)
            ]
            # filter out students, that are NOT selected, NOT blocked and are in the department
            interested_students = [
                s.email
                for s in Student.objects.filter(
                    is_blocked=False,
                    is_selected=False,
                    department__in=opening_departments,
                )
                # if s.email != ""
            ]
            # make multiple message bodies from queryset and use send_mass_mail
            print(interested_students)
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
