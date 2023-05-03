from django.contrib import admin
from user import models as m
from django.contrib.auth.admin import UserAdmin as UserAdmin_
from django.utils.translation import gettext_lazy as _
from tnpapp.admin import CustomUserAdmin


@admin.register(m.Admin)
class AdminUserAdmin(CustomUserAdmin):
    # Overrides the default username exclude for other
    # models in this app
    default_exclude = ()
    new_add_fields = ("email",)


@admin.register(m.Student)
class StudentAdmin(CustomUserAdmin):
    new_fields = (
        "phone_number",
        "enrollment_number",
        "marks",
        "institute",
        "department",
        "semester",
        "batch_year",
        "is_blocked",
        "is_selected",
    )

    new_add_fields = ("email",)

    readonly_fields = (
        "is_selected",
        "is_profile_complete",
    )

    new_list_filters = (
        "is_selected",
        "is_profile_complete",
        "is_blocked",
    )


@admin.register(m.Volunteer)
class VolunteerAdmin(CustomUserAdmin):
    new_fields = (
        "phone_number",
        # "job_numbers",
        "enrollment_number",
        "department",
        "semester",
        "volunteer_type",
        "reference",
    )

    new_add_fields = ("email",)


@admin.register(m.DeptOfficer)
class DeptOfficerAdmin(CustomUserAdmin):
    new_fields = (
        "phone_number",
        "department",
        "address",
    )

    new_add_fields = ("email",)
