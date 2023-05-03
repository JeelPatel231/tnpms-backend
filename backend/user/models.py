from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from user.roles import Department, VolunteerType
from tnpapp.models import CustomUser, UserRoles
import datetime
from typing import Tuple
from user.validators import number_validator
from functools import partial


# ALL USER MODELS
class AdminUserManager(UserManager):
    def get_queryset(self) -> models.QuerySet[AbstractUser]:
        return super().get_queryset().filter(is_superuser=True)


class Admin(CustomUser):
    objects = AdminUserManager()

    class Meta:
        proxy = True
        verbose_name = "Admin"
        verbose_name_plural = "Admins"

    def save(self, *args, **kwargs) -> None:
        """
        `self.pk` // primary key doesnt exist when model
        is not yet saved in database
        """
        if not self.pk:
            self.is_staff = True
            self.is_superuser = True
            # is_approved will be used if Custom User is extending
            # Approvable Mixin, else its just phantom data
            self.is_approved = True
        self.role = UserRoles.Admin
        return super().save(*args, **kwargs)


def calculate_semester(enrollment_number: str) -> Tuple[int, int]:
    today = datetime.datetime.now()

    current_year = today.year // 100 * 100
    year = current_year + int(enrollment_number[:2])
    last_3_digits = int(enrollment_number[-3:])
    sem = (today.year - year) * 2

    if today.month > 5:
        sem += 1
    if last_3_digits > 500:
        sem += 2
    return (year, sem)


class Student(CustomUser):
    enrollment_number = models.CharField(
        max_length=12, validators=[partial(number_validator, length=12)], unique=True
    )
    marks = models.IntegerField(blank=True, null=True)
    institute = models.CharField(
        max_length=3, validators=[partial(number_validator, length=3)]
    )
    department = models.PositiveSmallIntegerField(choices=Department.choices)
    semester = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)]
    )
    batch_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(2012),
            MaxValueValidator(datetime.datetime.now().year),
        ]
    )
    is_profile_complete = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_selected = models.BooleanField(default=False)
    _predefined_permissions = ["view_student"]

    def save(self, *args, **kwargs) -> None:
        self.role = UserRoles.Student
        if not self.pk:
            enr = self.enrollment_number
            batch_year, semester = calculate_semester(enr)

            self.username = f"S-{enr}"

            if not self.department:
                self.department = int(enr[7:9])
            if not self.batch_year:
                self.batch_year = batch_year
            if not self.institute:
                self.institute = enr[2:5]
            if not self.semester:
                self.semester = semester
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Volunteer(CustomUser):
    # why was this needed in the first place?
    # job_numbers = models.PositiveSmallIntegerField()
    enrollment_number = models.CharField(
        max_length=12, validators=[partial(number_validator, length=12)], unique=True
    )
    department = models.PositiveSmallIntegerField(choices=Department.choices)
    semester = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)]
    )
    volunteer_type = models.PositiveSmallIntegerField(
        choices=VolunteerType.choices, default=VolunteerType.WORKER
    )
    reference = models.TextField(max_length=2000, blank=True, null=True)

    _predefined_permissions = ["view_volunteer"]

    def save(self, *args, **kwargs) -> None:
        self.role = UserRoles.Volunteer
        if not self.pk:
            self.is_staff = True
            enr = self.enrollment_number
            self.username = f"V-{enr}"
            if not self.department:
                self.department = int(enr[7:9])
            if not self.semester:
                self.semester = calculate_semester(2000 + int(enr[0:2]))

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Volunteer"
        verbose_name_plural = "Volunteers"


class DeptOfficer(CustomUser):
    department = models.CharField(max_length=256)
    address = models.TextField(max_length=2000)

    _predefined_permissions = ["view_deptofficer"]

    def save(self, *args, **kwargs) -> None:
        self.role = UserRoles.DepartmentOfficer
        self.is_staff = True
        self.username = self.email
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Department Officer"
        verbose_name_plural = "Department Officers"
