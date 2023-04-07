from django.db import models
from company.roles import CompanyType, Gender
from user.roles import Department
from user.validators import number_validator
from functools import partial

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=256)
    email_id = models.EmailField()
    phone_number = models.CharField(
        max_length=10, validators=[partial(number_validator, length=10)]
    )
    hr_name = models.CharField(max_length=256)
    address = models.TextField()
    company_relation = models.PositiveSmallIntegerField(choices=CompanyType.choices)
    # is mandatory in document but ONLY needed if company is a child
    parent_company_name = models.CharField(max_length=256, null=True)
    # possible to move to enum probably
    industry_type = models.CharField(max_length=256)
    current_employees = models.PositiveBigIntegerField()
    # possible to move to enum probably
    company_type = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"


class CurrentOpening(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=256)
    opening_year = models.CharField(max_length=256)
    # supposed to be numeric 15? what exactly is nature, in a 15 digit number?
    nature_of_job = models.CharField(
        max_length=15, validators=[partial(number_validator, length=15)]
    )
    short_description = models.CharField(max_length=256)
    long_description = models.TextField()
    min_qualification = models.PositiveIntegerField()
    specialization = models.CharField(max_length=256)
    special_skill_requirement = models.TextField()
    vacancy_count = models.PositiveIntegerField()
    # why number? possibly text about address
    vacancy_location = models.PositiveIntegerField()
    min_package = models.FloatField()
    max_package = models.FloatField()
    # supposed to be boolean, what about `ANY` type? nullable boolean?
    gender_preference = models.PositiveSmallIntegerField(choices=Gender.choices)

    def __str__(self) -> str:
        return self.job_title


class OpeningForDepartment(models.Model):
    opening_id = models.ForeignKey(CurrentOpening, on_delete=models.CASCADE)
    dept_id = models.PositiveSmallIntegerField(choices=Department.choices, null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.opening_id} for {self.dept_id}"
    
    class Meta:
        unique_together = ('opening_id', 'dept_id',)

