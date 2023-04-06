from django.urls import include, path
from rest_framework.routers import DefaultRouter
from user import views as v
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

router = DefaultRouter()
router.register(r"student", v.StudentCrudView, basename="student")
router.register(r"volunteer", v.VolunteerCrudView, basename="volunteer")

# urlpatterns = [
#     path("", include(router.urls)),
#     path("login/", v.login_user),
#     path("logout/", v.logout_user),
#     path("me/", v.get_user),
#     path(
#         "register/student/",
#         v.StudentRegistrationView.as_view(),
#         name="student-registration-view",
#     ),
#     path("resume/<str:username>", v.generate_resume),
# ]

urlpatterns = [
    path("test/", include(router.urls)),
    path("", login_required(v.HomeView.as_view()), name="home"),
    path("register/", TemplateView.as_view(template_name="registrationchoice.html")),
    path(
        "student/resume/",
        TemplateView.as_view(template_name="student/resume.html"),
        name="student-resume",
    ),
    path(
        "student/apply/",
        TemplateView.as_view(template_name="student/ApplyToOpenings.html"),
        name="student-apply-openings",
    ),
    path(
        "register/student/",
        v.StudentRegistrationDRF.as_view(),
        name="registration-student",
    ),
    path(
        "register/volunteer/",
        v.VolunteerRegistrationDRF.as_view(),
        name="registration-volunteer",
    ),
]
