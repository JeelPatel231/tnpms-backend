from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions as p
from django.contrib.auth import login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from tnpapp.serializers import CustomUserSerializer
from user import serializers as s
from user import models as m
from django.template import Context, Template
from xhtml2pdf import pisa  # type: ignore
from django.http import HttpResponse
from user.utils import link_callback
from tnpapp.models import BaseCrudModelViewSet
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class StudentCrudView(BaseCrudModelViewSet):
    serializer_class = s.StudentSerializer
    model_class = m.Student


class VolunteerCrudView(BaseCrudModelViewSet):
    serializer_class = s.VolunteerSerializer
    model_class = m.Volunteer


@swagger_auto_schema(methods=["post"], request_body=s.UserLoginSerializer)
@csrf_exempt
@api_view(["POST"])
def login_user(req: Request):
    srlzr = s.UserLoginSerializer(data=req.data)
    if not srlzr.is_valid():
        return Response(srlzr.errors, status=400)

    user = m.CustomUser.objects.filter(username=srlzr.validated_data["username"]).first()
    if user is None:
        return Response("User Not Found in System", status=404)

    if not user.check_password(srlzr.validated_data["password"]):
        return Response("Wrong password", status=401)

    login(req, user)
    return Response(status=200)


@api_view(["GET"])
@permission_classes([p.IsAuthenticated])
def logout_user(req: Request):
    logout(req)
    return Response(status=200)


@api_view(["GET"])
@permission_classes([p.IsAuthenticated])
def get_user(req: Request):
    serializer = CustomUserSerializer(req.user)
    return Response(serializer.data)


@api_view(["GET"])
def generate_resume(req: Request, username: str):
    user = m.Student.objects.filter(username=username).first()
    if user is None:
        return Response("User not Found", status=404)

    # dummy resume html template
    t = Template("<center><h1>{{ message }}</h1></center>.")

    # dummy context to render, dict is supposed to be
    # student details
    c = Context({"message": "Resume"})

    html = t.render(c)
    response = HttpResponse(content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{user.username}_resume.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    # if errors while generateing pdf, return error
    if pisa_status.err:
        return Response(f"We had some errors <pre>{html}</pre>", status=500)

    return response
