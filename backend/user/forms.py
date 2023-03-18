from user import models as m
from django.contrib.auth.forms import UserCreationForm


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = m.Student
        fields = (
            "username",
            "password1",
            "password2",
            "enrollment_number",
        )


class VolunteerRegistrationForm(UserCreationForm):
    class Meta:
        model = m.Volunteer
        fields = (
            "username",
            "password1",
            "password2",
            "enrollment_number",
            "volunteer_type",
        )
