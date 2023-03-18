from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from tnpapp.models import UserRoles

@login_required
def login_redirect(request):
    # if user if student, send them to profile page
    if request.user.role == UserRoles.Student:
        return redirect("home")
    # else send them to admin panel
    return redirect("/admin")

