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
    path("", login_required(TemplateView.as_view(template_name="home.html")), name="home"),
    path(
        "register/student/",
        v.StudentRegistrationView.as_view(),
        name="student-registration-view",
    ),
    path(
        "register/volunteer/",
        v.VolunteerRegistrationView.as_view(),
        name="volunteer-registration-view",
    ),
]
