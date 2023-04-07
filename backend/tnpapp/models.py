from typing import Any
from django.db import models
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from tnpapp.permissions import FineGrainedPermissions
from typing import List
from user.validators import number_validator
from django.contrib.auth.models import Permission
from functools import partial
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.


class UserRoles(models.IntegerChoices):
    Admin = 0, "Admin"
    DepartmentOfficer = 1, "Department Officer"
    Volunteer = 2, "Volunteer"
    Student = 3, "Student"


class CustomUserManager(UserManager):
    def create_superuser(self, *args, **kwargs):
        """
        This method is used when creating a superuser, eg from command line
        when initializing the FIRST admin superuser in system.
        Apply the role to avoid null role exception (mandatory field in schema)
        """
        kwargs["role"] = UserRoles.Admin
        return super().create_superuser(*args, **kwargs)


class CustomUser(AbstractUser):
    _predefined_permissions: List[str] = []
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=10,
        validators=[partial(number_validator, length=10)],
        blank=True,
        null=True,
    )
    role = models.PositiveSmallIntegerField(choices=UserRoles.choices)

    objects = CustomUserManager()

    def save(self, *args, **kwargs) -> None:
        saved_user = super().save(*args, **kwargs)
        # assigning permissions AFTER the user is added in the database
        # TODO: move to groups
        self.user_permissions.add(
            *[Permission.objects.get(codename=i) for i in self._predefined_permissions]
        )
        return saved_user


class BaseCrudModelViewSet(ModelViewSet):
    # TODO : smaller serializer for all listing view and
    # detialed serializer for one entity view
    serializer_class: Any
    model_class: Any
    permission_classes = [FineGrainedPermissions]
    http_method_names = [
        "get",
        "post",
        # "put",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    ]
    # for filtering
    # https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend

    def get_object(self):
        obj = get_object_or_404(self.model_class, id=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        """
        add is_approved here or is_active filter here
        filtering code below for reference, DO NOT USE IN PRODUCTION
        return self.model_class.objects.filter(**self.request.GET.dict())
        """
        return self.model_class.objects.all()
