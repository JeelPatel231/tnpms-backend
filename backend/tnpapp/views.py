from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from tnpapp.models import UserRoles
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from typing import Any


@login_required
def login_redirect(request):
    # if user if student, send them to profile page
    if request.user.role == UserRoles.Student:
        return redirect("student-dashboard")
    # else send them to admin panel
    return redirect("/admin")


# TODO : TEST PLEASE
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    # seperated since student and volunteer need username prefix change
    # but for admin and do, username is their email
    # numbers on the left MUST BE EQUAL to the tuple numbers in UserRoles class
    FormRoleChoices = [
        (3, "Student"),
        (2, "Volunteer"),
        (0, "Admin / DO"),
    ]

    role = forms.ChoiceField(choices=FormRoleChoices)
    username = UsernameField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    field_order = ("role", "username", "password")

    def clean(self) -> dict[str, Any]:
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        role = self.cleaned_data.get("role")

        if role == str(UserRoles.Student):
            username = f"S-{username}"

        if role == str(UserRoles.Volunteer):
            username = f"V-{username}"

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
