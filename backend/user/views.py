from django.shortcuts import redirect
from rest_framework.response import Response
from tnpapp.permissions import FineGrainedPermissions
from user import serializers as s
from user import models as m
from django.http import QueryDict
from user.permissions import IsOwnerOrReadOnly, Registerable
from tnpapp.models import BaseCrudModelViewSet, UserRoles
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
# Create your views here.

class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "student/home.html"
    
    def get(self, request):
        if request.user.role != UserRoles.Student:
            return redirect("login-redirect")
        user = m.Student.objects.get(pk=request.user.id)
        serializer = s.StudentSerializer(user)
        return Response({"serializer": serializer})

    def post(self, request):
        # clean the form data
        data = { x:y for x,y in request.data.items() if y != '' }
        serializer = s.StudentSerializer(instance=request.user,data=data, partial=True)
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
