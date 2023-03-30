from rest_framework import serializers
from user import models as m
from tnpapp.serializers import BaseUserModelSerializer


class StudentSerializer(BaseUserModelSerializer):
    # https://github.com/encode/django-rest-framework/issues/1926
    class Meta(BaseUserModelSerializer.Meta):
        model = m.Student
        extra_kwargs = {
            "is_selected": {"read_only": True},
            # TODO :  FIELD LEVEL PERMISSIONS, is_blocked should
            # only be editable by authorised people
            "is_blocked": {"read_only": True},
            "is_profile_complete": {"read_only": True},
            "institute": {"required": False},
            "department": {"required": False},
            "batch_year": {"required": False},
            "semester": {"required": False},
        }


class InitialStudentRegistration(StudentSerializer):
    class Meta:
        model = m.Student
        fields = (
            "enrollment_number",
            "password1",
            "password2",
        )


class DeptOfficerSerializer(BaseUserModelSerializer):
    class Meta(BaseUserModelSerializer.Meta):
        model = m.DeptOfficer


class VolunteerSerializer(BaseUserModelSerializer):
    class Meta(BaseUserModelSerializer.Meta):
        model = m.Volunteer
        extra_kwargs = {
            "department": {"required": False},
            "semester": {"required": False},
            "volunteer_type": {"required": False},
        }


class InitialVolunteerRegistration(VolunteerSerializer):
    class Meta:
        model = m.Volunteer
        fields = (
            "enrollment_number",
            "password1",
            "password2",
            "volunteer_type",
        )


# this class is only used in DRF API
# TODO : check if OG django login view accepts json requests
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=False)
    password = serializers.CharField(allow_blank=False)
