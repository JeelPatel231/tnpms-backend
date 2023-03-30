from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from tnpapp.permissions import FineGrainedPermissions
from user import serializers as s
from user import models as m
from django.template import Context, Template
from xhtml2pdf import pisa  # type: ignore
from django.http import HttpResponse
from user.permissions import IsOwnerOrReadOnly, Registerable
from user.utils import link_callback
from tnpapp.models import BaseCrudModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

# Create your views here.


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
