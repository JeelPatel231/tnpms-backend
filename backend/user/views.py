from enum import Enum
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework.response import Response
from tnpapp.permissions import FineGrainedPermissions
from user import serializers as s
from user import models as m
from django.http import HttpRequest, QueryDict
from user.permissions import IsOwnerOrReadOnly, Registerable
from tnpapp.models import BaseCrudModelViewSet, UserRoles
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from dataclasses import dataclass


@dataclass
class NavbarRoute:
    label: str
    icon: str
    named_url: str

    def __str__(self) -> str:
        return f'{"label" : "{self.label}", "icon":"{self.icon}", "named_url":"{self.named_url}" }'


# Create your views here.
class NavbarRoutes(Enum):
    HOME = NavbarRoute("Home", "home", "student-dashboard")
    PROFILE = NavbarRoute("Profile", "person", "student-profile")
    RESUME = NavbarRoute("Resume", "description", "student-resume")
    LOGOUT = NavbarRoute("Log Out", "logout", "logout")


NAMED_ROUTES_MAP = {
    "profile": "student-profile",
    "dashboard": "student-dashboard",
    "resume": "student-resume",  # ????? NOT WORKING, WHY IS THIS?????
}


def provide_global_context(request: HttpRequest):
    return {
        "navbar_routes": [i.value for i in NavbarRoutes],
        "activetab": NAMED_ROUTES_MAP.get(request.get_full_path().split("/")[1]),
    }


class ProfileView(APIView):
    swagger_schema = None
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "student/profile.html"

    def get(self, request):
        if request.user.role != UserRoles.Student:
            return redirect("login-redirect")
        user = m.Student.objects.get(pk=request.user.id)
        serializer = s.StudentSerializer(user)
        return Response({"serializer": serializer})

    def post(self, request):
        # clean the form data
        data = {x: y for x, y in request.data.items() if y != ""}
        serializer = s.StudentSerializer(instance=request.user, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"serializer": serializer})
        serializer.save()
        return self.get(request)


class StudentCrudView(BaseCrudModelViewSet):
    serializer_class = s.StudentSerializer
    model_class = m.Student
    # check for correct usage, bitwise operation or list elements
    permission_classes = [IsOwnerOrReadOnly | Registerable | FineGrainedPermissions]


class VolunteerCrudView(BaseCrudModelViewSet):
    serializer_class = s.VolunteerSerializer
    model_class = m.Volunteer

    permission_classes = [IsOwnerOrReadOnly | Registerable | FineGrainedPermissions]


class StudentRegistrationDRF(APIView):
    swagger_schema = None
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "studentregistration.html"

    def get(self, request):
        serializer = s.InitialStudentRegistration()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = s.InitialStudentRegistration(data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer})
        serializer.save()
        return redirect("login")


class VolunteerRegistrationDRF(APIView):
    swagger_schema = None
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "volunteerregistration.html"

    def get(self, request):
        serializer = s.InitialVolunteerRegistration()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = s.InitialVolunteerRegistration(data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer})
        serializer.save()
        return redirect("login")


### Template Render views'
@login_required
def student_resume(request: HttpRequest):
    return render(request, "student/resume.html", context={"activetab": "string"})


@login_required
def student_dashboard(request: HttpRequest):
    return render(request, "student/dashboard.html", context={})


@login_required
def student_apply_openings(request: HttpRequest):
    return render(request, "student/apply_openings.html", context={})
