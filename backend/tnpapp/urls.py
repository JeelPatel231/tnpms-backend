"""djangorest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from company.urls import router as company_router
from placement.urls import router as placement_router
from tnpapp.views import login_redirect, UserLoginForm
from django.contrib.auth.views import LoginView

# you can also declare urlpatterns in the respected modules and use include('appname.urls')
# here, everything is right at one place
urlpatterns = [
    path("", login_redirect, name="login-redirect"),
    path("admin/", admin.site.urls),
    path("users/", include("user.urls")),
    # path('job/', include(company_router.urls)),
    # path('placement/', include(placement_router.urls)),
    # path('openapi/', include('openapi.urls')),
    # override login route with our defined login route
    path("accounts/login/", LoginView.as_view(authentication_form=UserLoginForm)),
    path("accounts/", include("django.contrib.auth.urls")),
]
